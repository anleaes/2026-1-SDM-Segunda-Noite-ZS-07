from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from datetime import timedelta
from vaccineItens.models import VaccineItem
from .models import Vaccination
from rest_framework import viewsets
from .serializer import VaccinationSerializer
from .forms import VaccinationsForm
from animals.models import Animal 
from vaccines.models import Vaccine

# Create your views here.

class VaccinationViewSet(viewsets.ModelViewSet):
    queryset = Vaccination.objects.all()
    serializer_class = VaccinationSerializer

def is_admin_or_mod(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin_or_mod)
def add_vaccination(request):
    if request.method == 'POST':

        animal_id = request.POST.get('animal_id')
        data_aplicacao = request.POST.get('vaccinatedAt') 
        peso = request.POST.get('weight_at')

        vacinacao = Vaccination.objects.create(
            animal_id=animal_id,
            vaccinatedAt=data_aplicacao,
            weight_at=peso,
            employee_id=81 
        )
        
        vaccine_ids = request.POST.getlist('vaccine_ids')
        dosages = request.POST.getlist('dosages')
        
        from datetime import datetime
        data_obj = datetime.strptime(data_aplicacao, '%Y-%m-%d').date()
        try:
            data_validade = data_obj.replace(year=data_obj.year + 1)
        except ValueError:
            data_validade = data_obj.replace(year=data_obj.year + 1, day=28)
        
        print("VACINAS:", vaccine_ids, "DOSES:", dosages)
        for vac_id, dose in zip(vaccine_ids, dosages):
            if vac_id and dose: # Proteção extra contra linhas vazias
                VaccineItem.objects.create(
                    vaccination_id=vacinacao.id,
                    vaccines_id=vac_id,
                    dosage=dose,
                    expiration_date=data_validade
                )
                
        messages.success(request, "Vacinação cadastrada!")
        return redirect('vaccination:list_vaccinations', direction='management')


def list_vaccinations(request, direction):

    if request.method == 'POST':
        vaccination_id = request.POST.get('vaccination_id')
        if vaccination_id:
            vaccination = get_object_or_404(Vaccination, pk=vaccination_id)
            vaccination.save()
            return redirect('vaccinations:list_vaccinations', direction=direction)

    vaccinations = Vaccination.objects.all()
    
    all_animals = Animal.objects.all().order_by('name')
    all_vaccines = Vaccine.objects.all().order_by('name')
    
    animals_with_history = Animal.objects.filter(
        vaccination__isnull=False 
    ).distinct().prefetch_related(
        'vaccination_set',             
        'vaccination_set__vaccineitem_set',
        'vaccination_set__vaccineitem_set__vaccines'
    )

    context = {
        'vaccinations': vaccinations,
        'all_animals': all_animals,
        'all_vaccines': all_vaccines,
        'animals_with_history': animals_with_history,
    }
        
    if direction == 'management':
        template_name = 'vaccinations/list_vaccinations.html' 
        form_vaccinations = VaccinationsForm()
        context['form_vaccinations'] = form_vaccinations

    return render(request, template_name, context)
