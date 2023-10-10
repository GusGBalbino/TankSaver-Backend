
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from TankSaverAPI.api import viewsets
from TankSaverAPI import views

route = routers.DefaultRouter()

route.register(r'posto', viewsets.PostoViewSet, basename='posto')
route.register(r'funcionario', viewsets.FuncionarioViewSet, basename='funcionario')
route.register(r'custos', viewsets.CustosViewSet, basename='custos')
route.register(r'compra', viewsets.CompraViewSet, basename='compra')
route.register(r'venda', viewsets.VendaViewSet, basename='venda')
route.register(r'tipoDeCombustivel', viewsets.TipoCombustivelViewSet, basename='tipoDeCombustivel')
route.register(r'tipoDePagamento', viewsets.TipoDePagamentoViewSet, basename='tipoDePagamento')
route.register(r'historico', viewsets.HistoricoViewSet, basename='historico')
route.register(r'', viewsets.LoginViewSet, basename='login')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(route.urls)),
]
