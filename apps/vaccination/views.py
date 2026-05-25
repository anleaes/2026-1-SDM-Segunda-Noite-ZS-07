from django.shortcuts import render
from .models import Vaccination
from rest_framework import viewsets
from .serializer import VaccinationSerializer

# Create your views here.


class VaccinationViewSet(viewsets.ModelViewSet):
    queryset = Vaccination.objects.all()
    serializer_class = VaccinationSerializer
