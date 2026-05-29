from django.shortcuts import render
from .models import Animal
from rest_framework import viewsets
from .serializer import AnimalSerializer

# Create your views here.
class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

def list_animals(request):
    template_name = 'animals/list_animals.html'
    animals = Animal.objects.filter(adopted=False)
    context={
        'animals': animals
    }
    return render(request, template_name, context)