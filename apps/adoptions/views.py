from django.shortcuts import render
from rest_framework import viewsets
from .models import Adoption
from .serializer import AdoptionSerializer

# Create your views here.

class AdoptionViewSet(viewsets.ModelViewSet):
    queryset = Adoption.objects.all()
    serializer_class = AdoptionSerializer