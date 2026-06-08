from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Animal
from species.models import Specie
from characteristics.models import Characteristic
from rest_framework import viewsets
from .serializer import AnimalSerializer
from .forms import AnimalForm

# Create your views here.

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    queryset = Animal.objects.select_related(
        'breed', 'breed__specie'
    ).prefetch_related(
        'characteristic',
        'vaccination_set__vaccineitem_set__vaccines'
    ).all()

def is_admin_or_mod(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin_or_mod)
def add_animal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
             
    return redirect('animals:list_animals', direction='management')

def list_animals(request, direction):
    if request.method == 'POST':
        animal_id = request.POST.get('animal_id')
        if animal_id:
            animal = get_object_or_404(Animal, pk=animal_id)
            animal.sterilized = request.POST.get('sterilized') == 'on'
            animal.adopted = request.POST.get('adopted') == 'on'
            animal.save()
            return redirect('animals:list_animals', direction=direction)

    animals = Animal.objects.all()
    species = Specie.objects.all()
    characteristics = Characteristic.objects.all()
    context = {
        'animals': animals,
        'species': species,
        'characteristics': characteristics,
    }
        
    if direction == 'management':
        template_name = 'animals/list_animals_management.html'
        form_animals = AnimalForm()
        context['form_animals'] = form_animals
    elif direction == 'all':
        template_name = 'animals/list_animals.html'

    return render(request, template_name, context)

def animal_detail(request, pk):
    template_name = 'animals/animal_detail.html'
    animal = get_object_or_404(
        Animal.objects.select_related(
            'breed', 'breed__specie').prefetch_related('characteristic'),
        pk=pk
    )
    return render(request, template_name, {'animal': animal})

@user_passes_test(is_admin_or_mod)
def edit_animal(request, id_animal):
    animal = get_object_or_404(Animal, id=id_animal)
    if request.method == 'POST':

        if 'quick_status_update' in request.POST:
            animal.sterilized = request.POST.get('sterilized') == 'on'
            animal.adopted = request.POST.get('adopted') == 'on'
            animal.save()
            return redirect('animals:list_animals', direction='management')
        
        if 'quick_characteristics_update' in request.POST:
            animal.characteristic.set(request.POST.getlist('characteristics'))
            return redirect('animals:list_animals', direction='management')
        
        form = AnimalForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            return redirect('animals:list_animals', direction='management')
        
    return redirect('animals:list_animals', direction='management')