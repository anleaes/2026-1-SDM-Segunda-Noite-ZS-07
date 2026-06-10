from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from .forms import EmployeeForm
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.contrib.auth.decorators import login_required, user_passes_test
from .serializer import EmployeeSerializer
from django.db import transaction
from django.contrib.auth.models import User

# Create your views here.
class EmployeeViewSet(viewsets.ModelViewSet):
   queryset = Employee.objects.all()
   serializer_class = EmployeeSerializer
   authentication_classes = [TokenAuthentication, SessionAuthentication]
   permission_classes = [IsAuthenticated, IsAdminUser]

   def create(self, request, *args, **kwargs):
        data = request.data
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=data.get('username'),
                    email=data.get('email'),
                    password=data.get('password'),
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name')
                )
                
                employee = Employee.objects.create(
                    user=user,
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    cpf=data.get('cpf'),
                    position=data.get('position'),
                    birth_date=data.get('birth_date'),
                    hire_date=data.get('hire_date'),
                    is_active=True
                )

                serializer = self.get_serializer(employee)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            print('esse é o erro', e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

   @action(detail=False, methods=['get'])
   def me(self, request):
        employee = get_object_or_404(Employee, user=request.user)
        serializer = self.get_serializer(employee)
        return Response(serializer.data)

   @action(detail=True, methods=['patch'])
   def alterar_cargo(self, request, pk=None):
        employee = self.get_object()
        novo_cargo = request.data.get('position')
        novo_nivel = request.data.get('role')

        if novo_cargo:
            employee.position = novo_cargo
            employee.save()

        if novo_nivel:
            user = employee.user

            if novo_nivel == 'Administrador':
                user.is_superuser = True
                user.is_staff = True
            elif novo_nivel == 'Moderador':
                user.is_superuser = False
                user.is_staff = True
            user.save()

        return Response({"status": "Cargo e nível atualizados com sucesso!"})
   
   @action(detail=True, methods=['patch'])
   def alterar_username(self, request, pk=None):
        employee = self.get_object()
        user = employee.user
        
        if not user:
            return Response({"error": "Este adotante não possui um usuário de login vinculado."}, status=status.HTTP_400_BAD_REQUEST)
            
        novo_username = request.data.get('username')
        if not novo_username:
            return Response({"error": "O novo nome de usuário não foi informado."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=novo_username).exclude(id=user.id).exists():
            return Response({"error": "Este nome de usuário já está em uso por outra pessoa."}, status=status.HTTP_400_BAD_REQUEST)
            
        user.username = novo_username
        user.save()
        return Response({"status": "Nome de usuário atualizado com sucesso!"})

   @action(detail=True, methods=['patch'])
   def alterar_senha(self, request, pk=None):
        employee = self.get_object()
        nova_senha = request.data.get('new_password')

        if request.user != employee.user and not request.user.is_superuser:
            return Response(
                {"error": "Apenas administradores podem alterar senhas de outros utilizadores."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        if not nova_senha:
            return Response({"error": "Nova senha não fornecida."}, status=status.HTTP_400_BAD_REQUEST)

        user = employee.user
        user.set_password(nova_senha)
        user.save()

        return Response({"status": "Senha atualizada com sucesso!"})

def is_admin_or_mod(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin_or_mod)
def add_employee(request):
    template_name = 'core:management_panel'
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():

            if User.objects.filter(username=form.cleaned_data.get('username')).exists():
                return Response(
                    {"error": "Este nome de utilizador já está em uso."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                user = User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    email=form.cleaned_data.get('email'),
                    password=form.cleaned_data.get('password'),
                    first_name=form.cleaned_data.get('first_name'),
                    last_name=form.cleaned_data.get('last_name')
                )
                
                employee = Employee.objects.create(
                    user=user,
                    first_name=form.cleaned_data.get('first_name'),
                    last_name=form.cleaned_data.get('last_name'),
                    cpf=form.cleaned_data.get('cpf'),
                    position=form.cleaned_data.get('position'),
                    birth_date=form.cleaned_data.get('birth_date'),
                    hire_date=form.cleaned_data.get('hire_date'),
                    is_active=True
                )

             
    return redirect(template_name)

def list_employees(request):
    template_name = 'employees/list_employees.html'
    employees = Employee.objects.filter()
    context = {
        'employees': employees,
    }
    return render(request, template_name, context)

def edit_employee(request, register_employee):
    template_name = 'core:management_panel'
    context ={}
    employee = get_object_or_404(Employee, register=register_employee)
    if request.method == 'POST':

        if 'quick_status_update' in request.POST:
            employee.is_active = request.POST.get('is_active') == 'on'
            employee.save()
            return redirect('core:management_panel')
        
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('core:management_panel')
    form = EmployeeForm(instance=employee)
    context['form'] = form
    return render(request, template_name, context)

def delete_employee(request, register_employee):
    employee = Employee.objects.get(register=register_employee)
    employee.delete()
    return redirect('employees:list_employees')