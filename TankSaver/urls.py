
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from TankSaverAPI.api import viewsets
from TankSaverAPI import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

route = routers.DefaultRouter()

route.register(r'', viewsets.LoginViewSet, basename='login')
route.register(r'posto', viewsets.PostoViewSet, basename='posto')
route.register(r'funcionario', viewsets.FuncionarioViewSet, basename='funcionario')
route.register(r'custos', viewsets.CustosViewSet, basename='custos')
route.register(r'compra', viewsets.CompraViewSet, basename='compra')
route.register(r'venda', viewsets.VendaViewSet, basename='venda')
route.register(r'tipoDeCombustivel', viewsets.TipoCombustivelViewSet, basename='tipoDeCombustivel')
route.register(r'tipoDePagamento', viewsets.TipoDePagamentoViewSet, basename='tipoDePagamento')
route.register(r'historico', viewsets.HistoricoViewSet, basename='historico')
route.register(r'responsavel', viewsets.ResponsavelViewSet, basename='responsavel')
route.register(r'taxas', viewsets.TaxasViewSet, basename='taxas')

schema_view = get_schema_view(
   openapi.Info(
      title="TankSaver APIs",
      default_version='v1.0',
      description="Documentação de todos os endpoints necessários para a criação do Tanksaver.",

   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('responsavel/<int:pk>/dadosPerfil/', viewsets.ResponsavelViewSet.as_view({'get': 'dadosPerfil'}), name='responsavel-dados-perfil'),
    path('funcionario/<int:pk>/funcionariosPorPosto/', viewsets.FuncionarioViewSet.as_view({'get': 'funcionariosPorPosto'}), name='funcionarios-por-posto'),
    path('custos/<int:pk>/custosPorPosto/', viewsets.CustosViewSet.as_view({'get': 'custosPorPosto'}), name='custos-por-posto'),
    path('compras/<int:pk>/comprasPorposto/', viewsets.CompraViewSet.as_view({'get': 'comprasPorPosto'}), name='compras-por-posto'),
    path('vendas/<int:pk>/vendasPorPosto/', viewsets.VendaViewSet.as_view({'get': 'vendasPorPosto'}), name='vendas-por-posto'),
    path('taxas/<int:pk>/taxasPorPosto/', viewsets.TaxasViewSet.as_view({'get': 'taxasPorPosto'}), name='taxas-por-posto'),
    path('historico/<int:pk>/historicoPorPosto/', viewsets.HistoricoViewSet.as_view({'get': 'historicoPorPosto'}), name='historico-por-posto'),
    path('tipoDePagamento/<int:pk>/pagamentoPorPosto/', viewsets.TipoDePagamentoViewSet.as_view({'get': 'pagamentoPorPosto'}), name='pagamento-por-posto'),
    path('', include(route.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
