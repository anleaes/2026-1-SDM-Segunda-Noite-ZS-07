from django.shortcuts import render, redirect
from rest_framework import viewsets
from .serializer import BreedSerializer
from .models import Breed
from species.models import Specie

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
    
def add_breed(request):
    template_name = 'breeds/add_breed.html'
    if request.method == 'POST':
        name = request.POST.get('name')
        specie_id = request.POST.get('specie')
        
        if name and specie_id:
            specie_obj = Specie.objects.get(id=specie_id)
            Breed.objects.create(name=name, specie=specie_obj)
            
            return redirect('breeds:add_breed') 

    species_list = Specie.objects.all()

    context = {
        'species': species_list
    }
    return render(request, template_name, context)