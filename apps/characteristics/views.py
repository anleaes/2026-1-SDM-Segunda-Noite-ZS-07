from django.shortcuts import render
from .models import Characteristic
from rest_framework import viewsets
from .serializer import CharacteristicSerializer

# Create your views here.
class CharacteristicViewSet(viewsets.ModelViewSet):
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicSerializer