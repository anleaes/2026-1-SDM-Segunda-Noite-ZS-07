from django.shortcuts import render
from rest_framework import viewsets
from .models import Specie
from .serializer import SpecieSerializer

# Create your views here.

class SpecieViewSet(viewsets.ModelViewSet):
    queryset = Specie.objects.all()
    serializer_class = SpecieSerializer