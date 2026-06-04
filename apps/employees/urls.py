from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'employees'

router = routers.SimpleRouter()
router.register('', views.EmployeeViewSet, basename='funcionarios')

urlpatterns = [
    path('', include(router.urls)),
    path('listar/', views.list_employees, name='list_employees'),
    path('adicionar/', views.add_employee, name='add_employee'),
    path('editar/<int:register_employee>/', views.edit_employee, name='edit_employee'),
    path('excluir/<int:register_employee>/', views.delete_employee, name='delete_employee'),
]
