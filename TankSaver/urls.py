"""
URL configuration for TankSaver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from rest_framework import routers
from TankSaverAPI.api import viewsets

route = routers.DefaultRouter()

route.register(r'Posto', viewsets.PostoViewSet, basename='Posto')
route.register(r'Funcionario', viewsets.FuncionarioViewSet, basename='Funcionario')
route.register(r'Custos', viewsets.CustosViewSet, basename='Custos')
route.register(r'Compra', viewsets.CompraViewSet, basename='Compra')
route.register(r'Venda', viewsets.VendaViewSet, basename='Venda')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(route.urls))
]
