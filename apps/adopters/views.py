from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.contrib.auth.models import User
from .models import Adopter
from .forms import AdopterForm
from .serializer import AdopterSerializer

# Create your views here.
class AdopterViewSet(viewsets.ModelViewSet):
    queryset = Adopter.objects.all()
    serializer_class = AdopterSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        data = request.data
        
        try:
            
            if User.objects.filter(username=data.get('username')).exists():
                return Response(
                    {"error": "Este nome de utilizador já está em uso."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                user = User.objects.create_user(
                    username=data.get('username'),
                    email=data.get('email'),
                    password=data.get('password'),
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name')
                )
                
                adopter = Adopter.objects.create(
                    user=user,
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    cpf=data.get('cpf'),
                    address=data.get('address'),
                    yard_security=data.get('yard_security', False),
                    addressComprove=data.get('addressComprove', False),
                    checkedData=data.get('checkedData', False),
                )
                
                serializer = self.get_serializer(adopter)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            print(f"======== ERRO NO CADASTRO DE CLIENTE: {str(e)} ========")
            return Response({"error": f"Falha no servidor: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def alterar_username(self, request, pk=None):
        adopter = self.get_object()
        user = adopter.user
        
        if not user:
            return Response({"error": "Este adotante não possui um usuário de login vinculado."}, status=status.HTTP_400_BAD_REQUEST)
            
        novo_username = request.data.get('username')
        if not novo_username:
            return Response({"error": "O novo nome de usuário não foi informado."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=novo_username).exclude(id=user.id).exists():
            return Response({"error": "Este nome de usuário já está em uso por outra pessoa."}, status=status.HTTP_400_BAD_REQUEST)
            
        user.username = novo_username
        user.save()
        return Response({"status": "Nome de usuário atualizado com sucesso!"})

    @action(detail=True, methods=['patch'])
    def alterar_senha(self, request, pk=None):
        if not request.user.is_superuser:
            return Response({"error": "Apenas administradores podem alterar senhas de clientes."}, status=status.HTTP_403_FORBIDDEN)
            
        adopter = self.get_object()
        user = adopter.user
        
        if not user:
            return Response({"error": "Este adotante não possui um usuário de login vinculado."}, status=status.HTTP_400_BAD_REQUEST)
            
        nova_senha = request.data.get('new_password')
        if not nova_senha:
            return Response({"error": "Nova senha não fornecida."}, status=status.HTTP_400_BAD_REQUEST)
            
        user.set_password(nova_senha)
        user.save()
        return Response({"status": "Senha do cliente atualizada com sucesso!"})
    
    @action(detail=True, methods=['patch'])
    def alterar_endereco(self, request, pk=None):
        adopter = self.get_object()
        
        novo_endereco = request.data.get('address')
        if not novo_endereco:
            return Response({"error": "O novo endereço não foi informado."}, status=status.HTTP_400_BAD_REQUEST)
            
        adopter.address = novo_endereco
        adopter.save()
        
        return Response({"status": "Endereço do cliente atualizado com sucesso!"})
    
def is_admin_or_mod(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin_or_mod)
def add_adopter(request):
    template_name = 'core:management_panel'
    if request.method == 'POST':
        form = AdopterForm(request.POST)
        if form.is_valid():
            
            if User.objects.filter(username=form.cleaned_data.get('username')).exists():
                return Response(
                    {"error": "Este nome de utilizador já está em uso."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            with transaction.atomic():
                user = User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    email=form.cleaned_data.get('email'),
                    password=form.cleaned_data.get('password'),
                    first_name=form.cleaned_data.get('first_name'),
                    last_name=form.cleaned_data.get('last_name')
                )
                
                adopter = Adopter.objects.create(
                    user=user,
                    first_name=form.cleaned_data.get('first_name'),
                    last_name=form.cleaned_data.get('last_name'),
                    cpf=form.cleaned_data.get('cpf'),
                    address=form.cleaned_data.get('address'),
                    yard_security=form.cleaned_data.get('yard_security', False),
                    addressComprove=form.cleaned_data.get('addressComprove', False),
                    checkedData=form.cleaned_data.get('checkedData', False),
                )
             
    return redirect(template_name)

@user_passes_test(is_admin_or_mod)
def edit_adopter(request, register_adopter):
    template_name = 'core:management_panel'
    adopter = get_object_or_404(Adopter, register=register_adopter)
    if request.method == 'POST':

        if 'quick_status_update' in request.POST:
            adopter.yard_security = request.POST.get('yard_security') == 'on'
            adopter.addressComprove = request.POST.get('address_verify') == 'on'
            adopter.checkedData = request.POST.get('checked_data') == 'on'
            adopter.save()
            return redirect('core:management_panel')
        
        form = AdopterForm(request.POST, instance=adopter)
        if form.is_valid():
            form.save()
            return redirect('core:management_panel')
        
    return redirect(template_name)