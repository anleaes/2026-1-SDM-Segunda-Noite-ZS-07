from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'animals'

router = routers.SimpleRouter()
router.register('', views.AnimalViewSet, basename='animais')

urlpatterns = [
    path('listar/', views.list_animals, name='list_animals'),
    path('', include(router.urls) ),
]