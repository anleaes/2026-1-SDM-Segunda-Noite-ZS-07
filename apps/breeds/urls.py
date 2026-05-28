from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'breeds'

router = routers.SimpleRouter()
router.register('', views.BreedViewSet, basename='racas')

urlpatterns = [
    path('', include(router.urls) )
]