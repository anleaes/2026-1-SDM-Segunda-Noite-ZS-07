from django.shortcuts import render
from animals.models import Animal

# Create your views here.

def home(request):
    template_name ='core/home.html'
    animals = Animal.objects.filter(adopted=False).prefetch_related('characteristic')
    context = {
        'animals': animals
    }
    return render(request, template_name, context)