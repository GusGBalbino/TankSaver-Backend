from rest_framework import viewsets
from TankSaverAPI.api import serializer
from TankSaverAPI import models

class PostoViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.PostoSerializer
    queryset = models.Posto.objects.all()

class FuncionarioViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.FuncionarioSerializer
    queryset = models.Funcionario.objects.all()

class CustosViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.CustosSerializer
    queryset = models.Custos.objects.all()

class CompraViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.CompraSerializer
    queryset = models.Compra.objects.all()

class VendaViewSet(viewsets.ModelViewSet):
    serializer_class = serializer.VendaSerializer
    queryset = models.Venda.objects.all()