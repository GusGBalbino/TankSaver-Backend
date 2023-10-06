
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from TankSaverAPI.api import viewsets
from TankSaverAPI import views

route = routers.DefaultRouter()

route.register(r'Posto', viewsets.PostoViewSet, basename='Posto')
route.register(r'Funcionario', viewsets.FuncionarioViewSet, basename='Funcionario')
route.register(r'Custos', viewsets.CustosViewSet, basename='Custos')
route.register(r'Compra', viewsets.CompraViewSet, basename='Compra')
route.register(r'Venda', viewsets.VendaViewSet, basename='Venda')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(route.urls)),
    path('login/', views.LoginView.as_view(), name="login"),
    path('compra/', views.CompraCreateView.as_view(), name="compra"),
    path('tipo-combustivel', views.TipoCombustivelList.as_view(), name="tipo-combustivel")
]
