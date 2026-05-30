from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from .forms import EmployeeForm
from rest_framework import viewsets
from .serializer import EmployeeSerializer

# Create your views here.
#class EmployeeViewSet(viewsets.ModelViewSet):
#    queryset = Employee.objects.all()
#    serializer_class = EmployeeSerializer

def add_employee(request):
    template_name = 'employees/add_employee.html'
    context = {}
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            return redirect('employees:list_employees')
    form = EmployeeForm()
    context['form'] = form
    return render(request, template_name, context)

def list_employees(request):
    template_name = 'employees/list_employees.html'
    employees = Employee.objects.filter()
    context = {
        'employees': employees,
    }
    return render(request, template_name, context)

def edit_employee(request, register_employee):
    template_name = 'employees/add_employee.html'
    context ={}
    employee = get_object_or_404(Employee, register=register_employee)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees:list_employees')
    form = EmployeeForm(instance=employee)
    context['form'] = form
    return render(request, template_name, context)

def delete_employee(request, register_employee):
    employee = Employee.objects.get(register=register_employee)
    employee.delete()
    return redirect('employees:list_employees')