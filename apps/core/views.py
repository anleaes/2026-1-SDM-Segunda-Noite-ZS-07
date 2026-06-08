from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from animals.models import Animal
from employees.models import Employee
from adopters.models import Adopter
from employees.forms import EmployeeForm
from adopters.forms import AdopterForm

# Create your views here.

def home(request):
    template_name ='core/home.html'

    all_animals = Animal.objects.all().prefetch_related('characteristic')
    animals = [animal for animal in all_animals if not animal.adopted]

    context = {
        'animals': animals
    }
    return render(request, template_name, context)

@user_passes_test(lambda u: u.is_superuser)
def management_panel(request):
    template_name = 'dashboard/management_panel.html'

    employees = Employee.objects.all()
    form_employee = EmployeeForm()
    adopters = Adopter.objects.all()
    form_adopters = AdopterForm()
    
    context = {
        'employees': employees,
        'adopters': adopters,
        'form_employee': form_employee,
        'form_adopters': form_adopters
    }
    return render(request, template_name, context)