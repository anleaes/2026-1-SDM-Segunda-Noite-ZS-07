from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'vaccines'

router = routers.SimpleRouter()
router.register('', views.VaccineViewSet, basename='vacinas')

urlpatterns = [
    path('', include(router.urls) )
]