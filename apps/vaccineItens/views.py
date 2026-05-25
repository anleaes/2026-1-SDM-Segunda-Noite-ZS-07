from django.shortcuts import render
from .models import VaccineItem
from rest_framework import viewsets
from .serializer import VaccineItemSerializer

# Create your views here.


class VaccineItemViewSet(viewsets.ModelViewSet):
    queryset = VaccineItem.objects.all()
    serializer_class = VaccineItemSerializer
