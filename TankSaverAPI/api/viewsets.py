from rest_framework import viewsets
from TankSaverAPI.api import serializer
from TankSaverAPI import models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class PostoViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.PostoSerializer
    queryset = models.Posto.objects.all()

class FuncionarioViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.FuncionarioSerializer
    queryset = models.Funcionario.objects.all()

class CustosViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.CustosSerializer
    queryset = models.Custos.objects.all()

class CompraViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.CompraSerializer
    queryset = models.Compra.objects.all()

    def create(self, request):
        data = request.data
        # data['posto'] = request.user.id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendaViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.VendaSerializer
    queryset = models.Venda.objects.all()
    
class TipoCombustivelViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.TipoCombustivelSerializer
    queryset = models.TipoCombustivel.objects.all()

class TipoDePagamentoViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.TipoDePagamentoSerealizer
    queryset = models.TipoCombustivel.objects.all()