from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', TemplateView.as_view(template_name='core/login.html'), name='login'),


]
