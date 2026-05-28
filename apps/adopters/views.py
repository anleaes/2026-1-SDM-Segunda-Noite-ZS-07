from django.shortcuts import render
from .models import Adopter
from rest_framework import viewsets
from .serializer import AdopterSerializer

# Create your views here.
class AdopterViewSet(viewsets.ModelViewSet):
    queryset = Adopter.objects.all()
    serializer_class = AdopterSerializer 