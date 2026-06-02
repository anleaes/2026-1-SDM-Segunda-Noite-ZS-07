import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from .forms import UserForm, UserChangeInformationForm

# Create your views here.


@csrf_exempt
def add_user(request):
    if request.content_type == 'application/json':
        if request.method != 'POST':
            return JsonResponse({'error': 'Método não permitido'}, status=405)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        form = UserForm(data)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key, 'username': user.username}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

    # Fluxo normal para o template HTML
    template_name = 'accounts/add_user.html'
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.set_password(f.password)
            f.save()
            return redirect('accounts:user_login')
        else:
            return redirect('accounts:add_user')
    form = UserForm()
    context['form'] = form
    return render(request, template_name, context)


@csrf_exempt
def user_login(request):
    is_api = request.content_type == 'application/json' or request.headers.get(
        'Accept') == 'application/json'
    if is_api:
        if request.method != 'POST':
            return JsonResponse({'error': 'Método não permitido'}, status=405)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key, 'username': user.username})
        return JsonResponse({'error': 'Usuário ou senha inválidos'}, status=401)

    # Fluxo normal para o template HTML
    template_name = 'accounts/user_login.html'
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        else:
            messages.error(request, 'Credenciais inválidas.')
            return redirect('accounts:user_login')
    return render(request, template_name, {})


@login_required(login_url='/contas/login/')
def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')


@login_required(login_url='/contas/login/')
def user_change_password(request):
    template_name = 'accounts/user_change_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
        else:
            return redirect('accounts:user_login')
    form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def user_change_information(request, username):
    template_name = 'accounts/user_change_information.html'
    context = {}
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = UserChangeInformationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    form = UserChangeInformationForm(instance=user)
    context['form'] = form
    return render(request, template_name, context)
