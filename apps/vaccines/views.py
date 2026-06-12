from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Vaccine
from rest_framework import viewsets
from .serializer import VaccineSerializer
from .forms import VaccinesForm

# Create your views here.
class VaccineViewSet(viewsets.ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer 

def is_admin_or_mod(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin_or_mod)
def add_vaccine(request):
    if request.method == 'POST':
        form = VaccinesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
             
    return redirect('vaccines:list_vaccines', direction='management')

def list_vaccines(request, direction):
    if request.method == 'POST':
        vaccine_id = request.POST.get('vaccine_id')
        if vaccine_id:
            vaccine = get_object_or_404(Vaccine, pk=vaccine_id)
            vaccine.save()
            return redirect('vaccines:list_vaccines', direction=direction)

    vaccines = Vaccine.objects.all()
    context = {
        'vaccines': vaccines,
    }
        
    if direction == 'management':
        template_name = 'vaccines/list_vaccines.html'
        form_vaccines = VaccinesForm()
        context['form_vaccines'] = form_vaccines

    return render(request, template_name, context)

@user_passes_test(is_admin_or_mod)
def edit_vaccine(request, id_vaccine):
    vaccine = get_object_or_404(Vaccine, id=id_vaccine)
    if request.method == 'POST':

        if 'quick_status_update' in request.POST:
            vaccine.save()
            return redirect('vaccines:list_vaccines', direction='management')
        
        form = VaccinesForm(request.POST, instance=vaccine)
        if form.is_valid():
            form.save()
            return redirect('vaccines:list_vaccines', direction='management')
        
    return redirect('vaccines:list_vaccines', direction='management')

@user_passes_test(is_admin_or_mod)
def delete_vaccine(request, id_vaccine):
    vaccine = get_object_or_404(Vaccine, id=id_vaccine)
    
    if request.method == 'POST':
        nome_vacina = vaccine.name
        vaccine.delete()
        messages.success(request, f'A vacina "{nome_vacina}" foi excluída com sucesso!')

        return redirect('vaccines:list_vaccines', direction='management')
    
    return redirect('vaccines:list_vaccines', direction='management')