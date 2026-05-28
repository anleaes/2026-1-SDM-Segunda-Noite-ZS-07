from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'adopters'

router = routers.SimpleRouter()
router.register('', views.AdopterViewSet, basename='adotantes')

urlpatterns = [
    path('', include(router.urls) )
]