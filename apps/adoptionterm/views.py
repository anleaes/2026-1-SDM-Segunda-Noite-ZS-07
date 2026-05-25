from django.shortcuts import render
from .models import Adoptionterm
from .serializer import AdoptiontermSerializer
from rest_framework import viewsets

# Create your views here.

class AdoptiontermViewSet(viewsets.ModelViewSet):
    queryset = Adoptionterm.objects.all()
    serializer_class = AdoptiontermSerializer