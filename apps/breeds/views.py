from django.shortcuts import render
from rest_framework import viewsets
from .serializer import BreedSerializer
from .models import Breed

# Create your views here.

class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer