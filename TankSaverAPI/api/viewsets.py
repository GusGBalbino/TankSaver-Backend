from rest_framework import viewsets, status
from TankSaverAPI.api import serializer
from TankSaverAPI import models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, date
from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction

class LoginViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get("email")
        senha = request.data.get("senha")

        posto = models.Posto.objects.filter(email=email).first()

        if posto and posto.senha == senha:  # Por enquanto, comparando senhas em texto plano
            refresh = RefreshToken.for_user(posto)
            access_token = str(refresh.access_token)
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)

        return Response({"Erro": "Login inválido"}, status=status.HTTP_401_UNAUTHORIZED)

class PostoViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.PostoSerializer
    queryset = models.Posto.objects.all()

class FuncionarioViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.FuncionarioSerializer
    queryset = models.Funcionario.objects.all()

    def criarFuncionario(self, request):
        data = request.data
        data['posto'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustosViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.CustosSerializer
    queryset = models.Custos.objects.all()

    def criarCustos(self, request):
        data = request.data
        data['posto'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompraViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.CompraSerializer
    queryset = models.Compra.objects.all()

    def criarCompra(self, request):
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
    
    def criarVenda(self, request):
        data = request.data
        data['posto'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TipoCombustivelViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.TipoCombustivelSerializer
    queryset = models.TipoCombustivel.objects.all()

class TipoDePagamentoViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.TipoDePagamentoSerealizer
    queryset = models.TipoPagamento.objects.all()

    def criarTipoPagamento(self, request):
        data = request.data
        data['posto'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class HistoricoViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = models.Historico.objects.all()
    serializer_class = serializer.HistoricoSerializer
    
    @action(detail=False, methods=['post'])
    def fecharMes(self, request):
        mes = request.data.get('mes', None)
        ano = request.data.get('ano', None)
        posto_id = request.data.get('posto_id')

        # Verifique se o posto_id é válido
        if not models.Posto.objects.filter(id=posto_id).exists():
            return Response({'Error': 'Invalid posto_id'}, status=status.HTTP_400_BAD_REQUEST)

        # Se mês e ano não forem fornecidos, defina-os como o mês e ano atuais
        if not mes or not ano:
            now = datetime.now()
            mes = now.month
            ano = now.year

        try:
            with transaction.atomic():
                # Calcula os valores para o histórico
                despesa_mensal = self._calcular_despesa(mes, ano, posto_id)
                faturamento_mensal = self._calcular_faturamento(mes, ano, posto_id)
                total_rendimento = faturamento_mensal - despesa_mensal

                # Atualiza ou cria o registro no histórico
                historico, created = models.Historico.objects.update_or_create(
                    data_historico=date(ano, mes, 1),  # Usando o primeiro dia do mês
                    posto_id=posto_id,
                    defaults={
                        'despesa_mensal': despesa_mensal,
                        'faturamento_mensal': faturamento_mensal,
                        'total_rendimento': total_rendimento
                    }
                )

            return Response(serializer.HistoricoSerializer(historico).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def _calcular_faturamento(self, mes, ano, posto_id):
        vendas = models.Venda.objects.filter(data_venda__year=ano, data_venda__month=mes, posto_id=posto_id)
        return sum(venda.volume_venda * venda.preco_litro for venda in vendas)
    
    def _calcular_despesa(self, mes, ano, posto_id):
        despesa_compras = self._calcular_despesa_compras(mes, ano, posto_id)
        total_taxas = self._calcular_total_taxas(posto_id)
        total_folha = self._calcular_total_folha(posto_id)
        total_custos = self._calcular_total_custos(posto_id)
    
        return despesa_compras + total_taxas + total_folha + total_custos

    def _calcular_despesa_compras(self, mes, ano, posto_id):
        compras = models.Compra.objects.filter(data_compra__year=ano, data_compra__month=mes, posto_id=posto_id)
        return sum(compra.volume_compra * compra.preco_litro for compra in compras)

    def _calcular_total_taxas(self, posto_id):
        taxas = models.Taxas.objects.filter(posto_id=posto_id).first()
        return sum([getattr(taxas, field.name) for field in taxas._meta.fields if field.name not in ['id', 'posto', 'posto_id']]) if taxas else 0

    def _calcular_total_folha(self, posto_id):
        funcionarios = models.Funcionario.objects.filter(posto_id=posto_id)
        return sum(funcionario.total_folha for funcionario in funcionarios)

    def _calcular_total_custos(self, posto_id):
        custos = models.Custos.objects.filter(posto_id=posto_id).first()
        return sum([getattr(custos, field.name) for field in custos._meta.fields if field.name not in ['id', 'posto', 'posto_id']]) if custos else 0


class ResponsavelViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.ResponsavelSerializer
    queryset = models.Responsavel.objects.all()

    def criarResponsavel(self, request):
        data = request.data
        data['posto'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnderecoViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.EnderecoSerializer
    queryset = models.Endereco.objects.all()

    def criarEndereco(self, request):
        data = request.data
        data['posto'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class TaxasViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializer.TaxasSerializer
    queryset = models.Taxas.objects.all()

    def criarTaxas(self, request):
        data = request.data
        data['posto'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)