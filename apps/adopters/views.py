from django.shortcuts import render, get_object_or_404, redirect
from .models import Adopter
from .forms import AdopterForm
from rest_framework import viewsets
from .serializer import AdopterSerializer

# Create your views here.
# class AdopterViewSet(viewsets.ModelViewSet):
#     queryset = Adopter.objects.all()
#     serializer_class = AdopterSerializer 

def add_adopter(request):
    template_name = 'adopters/add_adopter.html'
    context = {}
    if request.method == 'POST':
        form = AdopterForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            return redirect('adopters:list_adopters')
    form = AdopterForm()
    context['form'] = form
    return render(request, template_name, context)

def list_adopters(request):
    template_name = 'adopters/list_adopters.html'
    adopters = Adopter.objects.filter()
    context = {
        'adopters': adopters,
    }
    return render(request, template_name, context)

def edit_adopter(request, register_adopter):
    template_name = 'adopters/add_adopter.html'
    context ={}
    adopter = get_object_or_404(Adopter, register=register_adopter)
    if request.method == 'POST':
        form = AdopterForm(request.POST, instance=adopter)
        if form.is_valid():
            form.save()
            return redirect('adopters:list_adopters')
    form = AdopterForm(instance=adopter)
    context['form'] = form
    return render(request, template_name, context)

def delete_adopter(request, register_adopter):
    adopter = Adopter.objects.get(register=register_adopter)
    adopter.delete()
    return redirect('adopters:list_adopters')