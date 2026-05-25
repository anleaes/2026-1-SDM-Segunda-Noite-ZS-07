from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'vaccination'

router = routers.SimpleRouter()
router.register('', views.VaccinationViewSet, basename='vacinacoes')

urlpatterns = [
	path('', include(router.urls) )
]
