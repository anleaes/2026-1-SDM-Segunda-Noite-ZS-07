from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'animals'

router = routers.SimpleRouter()
router.register('', views.AnimalViewSet, basename='animais')

urlpatterns = [
    path('listar/<str:direction>/', views.list_animals, name='list_animals'),
    path('detalhes/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('editar/<int:id_animal>/', views.edit_animal, name='edit_animal'),
    path('adicionar/', views.add_animal, name='add_animal'),
    path('', include(router.urls)),
]
