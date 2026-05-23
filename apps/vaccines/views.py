from django.shortcuts import render
from .models import Vaccine
from rest_framework import viewsets
from .serializer import VaccineSerializer

# Create your views here.
class VaccineViewSet(viewsets.ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer 