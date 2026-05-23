from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'animals'

router = routers.SimpleRouter()
router.register('', views.AnimalViewSet, basename='animais')

urlpatterns = [
    path('', include(router.urls) )
]