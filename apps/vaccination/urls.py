from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'vaccination'

router = routers.SimpleRouter()
router.register('', views.VaccinationViewSet, basename='vacinacoes')

urlpatterns = [
    path('listar/<str:direction>/', views.list_vaccinations, name='list_vaccinations'),
    path('adicionar/', views.add_vaccination, name='add_vaccination'),
	path('', include(router.urls) )
]
