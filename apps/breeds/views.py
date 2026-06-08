from django.shortcuts import render
from rest_framework import viewsets
from .serializer import BreedSerializer
from .models import Breed

# Create your views here.

class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        specie_id = self.request.query_params.get('specie') 
        
        if specie_id:
            queryset = queryset.filter(specie_id=specie_id)
            
        return queryset