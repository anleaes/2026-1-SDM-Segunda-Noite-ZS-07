from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'adoptions'

router = routers.SimpleRouter()
router.register('', views.AdoptionViewSet, basename='adocoes')

urlpatterns = [
    path('form/<int:animal_id>/', views.adoption_form_page, name='adoption_form'),
    path('minhas-solicitacoes/', views.my_requests_page, name='my_requests'),
    path('solicitacoes/', views.adoption_requests_panel,
         name='adoption_requests_panel'),
    path('', include(router.urls))
]
