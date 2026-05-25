"""
URL configuration for adoptionapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pessoas/', include('persons.urls', namespace='persons')),
    path('especies/', include('species.urls', namespace='species')),
    path('funcionarios/', include('employees.urls', namespace='employees')),
    path('adotantes/', include('adopters.urls', namespace='adopters')),
    path('racas/', include('breeds.urls', namespace='breeds')),
    path('vacinas/', include('vaccines.urls', namespace='vaccines')),
    path('caracteristicas/', include('characteristics.urls', namespace='characteristics')),
    path('animais/', include('animals.urls', namespace='animals')),
    path('adocoes/', include('adoptions.urls', namespace='adoptions')),
    path('termos/', include('adoptionterm.urls', namespace='adoptionsterm')),
]
