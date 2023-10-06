from rest_framework import viewsets
from TankSaverAPI.api import serializer
from TankSaverAPI import models
from rest_framework.permissions import IsAuthenticated

class PostoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializer.PostoSerializer
    queryset = models.Posto.objects.all()

class FuncionarioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializer.FuncionarioSerializer
    queryset = models.Funcionario.objects.all()

class CustosViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializer.CustosSerializer
    queryset = models.Custos.objects.all()

class CompraViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializer.CompraSerializer
    queryset = models.Compra.objects.all()

class VendaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializer.VendaSerializer
    queryset = models.Venda.objects.all()
    
class TipoCombustivelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializer.TipoCombustivelSerializer
    queryset = models.TipoCombustivel.objects.all()