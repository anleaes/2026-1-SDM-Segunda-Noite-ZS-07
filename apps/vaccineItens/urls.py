from django.urls import path, include
from . import views
from rest_framework import routers



router = routers.SimpleRouter()
router.register('', views.VaccineItemViewSet, basename='itens_vacina')

urlpatterns = [
    path('', include(router.urls))
]
