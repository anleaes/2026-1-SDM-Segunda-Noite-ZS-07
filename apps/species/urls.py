from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'species'

router = routers.SimpleRouter()
router.register('', views.SpecieViewSet, basename='especies')

urlpatterns = [
    path('', include(router.urls) )
]