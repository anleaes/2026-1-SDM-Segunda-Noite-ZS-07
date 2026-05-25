from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'adoptionsterm'

router = routers.SimpleRouter()
router.register('', views.AdoptiontermViewSet, basename='termos_adocao')

urlpatterns = [
    path('', include(router.urls) )
]