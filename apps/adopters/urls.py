from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'adopters'

# router = routers.SimpleRouter()
# router.register('', views.AdopterViewSet, basename='adotantes')

urlpatterns = [
#    path('', include(router.urls) ),
    path('listar/', views.list_adopters, name='list_adopters'),
    path('adicionar/', views.add_adopter, name='add_adopter'),
    path('editar/<int:register>/', views.edit_adopter, name='edit_adopter'),
    path('excluir/<int:register>/', views.delete_adopter, name='delete_adopter'),
]