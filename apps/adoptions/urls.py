from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'adoptions'

router = routers.SimpleRouter()
router.register('', views.AdoptionViewSet, basename='adocoes')

urlpatterns = [
    path('', include(router.urls) )
]