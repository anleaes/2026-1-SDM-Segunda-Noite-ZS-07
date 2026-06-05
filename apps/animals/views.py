from django.shortcuts import render, get_object_or_404
from .models import Animal
from species.models import Specie
from characteristics.models import Characteristic
from rest_framework import viewsets
from .serializer import AnimalSerializer

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


def list_animals(request):
    template_name = 'animals/list_animals.html'
    animals = Animal.objects.filter(adopted=False)
    species = Specie.objects.filter()
    characteristics = Characteristic.objects.filter()
    context = {
        'animals': animals,
        'species': species,
        'characteristics': characteristics,
    }
    return render(request, template_name, context)


def animal_detail(request, pk):
    template_name = 'animals/animal_detail.html'
    animal = get_object_or_404(
        Animal.objects.select_related(
            'breed', 'breed__specie').prefetch_related('characteristic'),
        pk=pk
    )
    return render(request, template_name, {'animal': animal})
