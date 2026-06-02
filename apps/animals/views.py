from django.shortcuts import render
from .models import Animal
from species.models import Specie
from characteristics.models import Characteristic
from rest_framework import viewsets
from .serializer import AnimalSerializer

# Create your views here.
class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

def list_animals(request):
    template_name = 'animals/list_animals.html'
    animals = Animal.objects.filter(adopted=False)
    species = Specie.objects.filter()
    characteristics = Characteristic.objects.filter()
    context={
        'animals': animals,
        'species': species,
        'characteristics': characteristics,
    }
    return render(request, template_name, context)