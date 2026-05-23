from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'characteristics'

router = routers.SimpleRouter()
router.register('', views.CharacteristicViewSet, basename='caracteristicas')

urlpatterns = [
    path('', include(router.urls) )
]