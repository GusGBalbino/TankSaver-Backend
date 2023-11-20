from rest_framework import viewsets, status
from TankSaverAPI.api import serializer
from TankSaverAPI import models
from decimal import Decimal
from django.db import transaction
from TankSaverAPI.models import Posto
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from datetime import datetime, date
from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.contrib.auth.hashers import check_password
from .serializer import FuncionarioSerializer, CustosSerializer, VendaSerializer, CompraSerializer, TaxasSerializer, HistoricoSerializer

class LoginViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get("email")
        senha = request.data.get("senha")

        posto = Posto.objects.filter(email=email).first()

        if posto and check_password(senha, posto.senha): #Comparando a senha criptografada
            refresh = RefreshToken.for_user(posto)
            access_token = str(refresh.access_token)
            postoId = posto.pk
            postoName = posto.nome_fantasia
            return Response(
                {
                    "access_token": access_token, 
                    "postoId": postoId, 
                    "postoName": postoName
                }, status=status.HTTP_200_OK)

        return Response({"Erro": "Login inválido"}, status=status.HTTP_401_UNAUTHORIZED)

class PostoViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    serializer_class = serializer.PostoSerializer
    queryset = models.Posto.objects.all()

class FuncionarioViewSet(viewsets.ModelViewSet):
    ##permission_classes = [IsAuthenticated]
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
        
    
    @action(detail=True, methods=['get'])
    def funcionariosPorPosto(self, request, pk=None):
        funcionarios = models.Funcionario.objects.filter(posto_id=pk)
        serializer = FuncionarioSerializer(funcionarios, many=True)
        return Response(serializer.data)

class CustosViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
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
        
        
    @action(detail=True, methods=['get'])
    def custosPorPosto(self, request, pk=None):
        custos = models.Custos.objects.filter(posto_id=pk)
        serializer = CustosSerializer(custos, many=True)
        return Response(serializer.data)
    

class CompraViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
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
        
    
    @action(detail=True, methods=['get'])
    def comprasPorPosto(self, request, pk=None):
        compras = models.Compra.objects.filter(posto_id=pk)
        serializer = CompraSerializer(compras, many=True)
        return Response(serializer.data)

class VendaViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    serializer_class = serializer.VendaSerializer
    queryset = models.Venda.objects.all()
    
    def criarVenda(self, request):
        data = request.data
        tipo_pagamento_id = data.get('tipo_pagamento')
        volume_venda = Decimal(data.get('volume_venda'))
        preco_litro = Decimal(data.get('preco_litro'))

        try:
            tipo_pagamento = models.TipoPagamento.objects.get(id=tipo_pagamento_id)
            valor_venda_bruto = volume_venda * preco_litro
            taxa_pagamento = tipo_pagamento.taxa / 100

            # Aplicando a taxa do tipo de pagamento ao valor bruto
            valor_venda_liquido = valor_venda_bruto - (valor_venda_bruto * taxa_pagamento)

            # Atualizando os dados da venda com o valor líquido
            data['valor_venda'] = valor_venda_liquido

            # Criando o registro de venda
            with transaction.atomic():
                venda_serializer = self.get_serializer(data=data)
                if venda_serializer.is_valid():
                    venda_serializer.save()
                    headers = self.get_success_headers(venda_serializer.data)
                    return Response(venda_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                else:
                    return Response(venda_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.TipoPagamento.DoesNotExist:
            return Response({'error': 'Tipo de pagamento não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['get'])
    def vendasPorPosto(self, request, pk=None):
        vendas = models.Venda.objects.filter(posto_id=pk)
        serializer = VendaSerializer(vendas, many=True)
        return Response(serializer.data)
    
class TipoCombustivelViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    serializer_class = serializer.TipoCombustivelSerializer
    queryset = models.TipoCombustivel.objects.all()

class TipoDePagamentoViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    serializer_class = serializer.TipoDePagamentoSerializer
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
    ##permission_classes = [IsAuthenticated]
    queryset = models.Historico.objects.all()
    serializer_class = serializer.HistoricoSerializer

    def _get_date(self, mes=None, ano=None):
        if not mes or not ano:
            now = datetime.now()
            mes = now.month
            ano = now.year
        return mes, ano

    def _check_posto_id(self, posto_id):
        return models.Posto.objects.filter(id=posto_id).exists()

    @action(detail=False, methods=['post'])
    def fecharMes(self, request):
        mes, ano = self._get_date(request.data.get('mes'), request.data.get('ano'))
        posto_id = request.data.get('posto_id')
        
        if not self._check_posto_id(posto_id):
            return Response({'Error': 'Invalid posto_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                faturamento_mensal = self._calcular_faturamento(mes, ano, posto_id)
                total_taxas = self._calcular_total_taxas(posto_id, faturamento_mensal)
                despesa_compras = self._calcular_despesa_compras(mes, ano, posto_id)
                total_folha = self._calcular_total_folha(posto_id)
                total_custos = self._calcular_total_custos(posto_id)

                despesa_mensal = despesa_compras + total_folha + total_custos + total_taxas
                total_rendimento = faturamento_mensal - despesa_mensal

                historico, created = models.Historico.objects.update_or_create(
                    data_historico=date(ano, mes, 1),
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

    @action(detail=False, methods=['get'])
    def lucroMensal(self, request):
        mes, ano = self._get_date(request.query_params.get('mes'), request.query_params.get('ano'))
        posto_id = request.query_params.get('posto_id')

        if not self._check_posto_id(posto_id):
            return Response({'Error': 'Invalid posto_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            historico = models.Historico.objects.filter(
                data_historico__year=ano, 
                data_historico__month=mes, 
                posto_id=posto_id
            ).first()
            lucro = historico.total_rendimento if historico else 0
            return Response({"Lucro mensal": lucro}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'])
    def lucroAnual(self, request):
        ano = request.query_params.get('ano') or datetime.now().year
        posto_id = request.query_params.get('posto_id')

        if not self._check_posto_id(posto_id):
            return Response({'Error': 'Invalid posto_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            total_rendimento_anual = sum([
                models.Historico.objects.filter(
                    data_historico__year=ano, 
                    data_historico__month=mes, 
                    posto_id=posto_id
                ).first().total_rendimento for mes in range(1, 13)
                if models.Historico.objects.filter(
                    data_historico__year=ano, 
                    data_historico__month=mes, 
                    posto_id=posto_id
                ).exists()
            ])
            return Response({"Lucro anual": total_rendimento_anual}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
    @action(detail=True, methods=['get'])
    def historicoPorPosto(self, request, pk=None):
        historico = models.Historico.objects.filter(posto_id=pk)
        serializer = HistoricoSerializer(historico, many=True)
        return Response(serializer.data)

#FUNÇÕES AUXILIARES
        
    def _calcular_faturamento(self, mes, ano, posto_id):
        vendas = models.Venda.objects.filter(data_venda__year=ano, data_venda__month=mes, posto_id=posto_id)
        
        faturamento_total = 0
        for venda in vendas:
            valor_bruto = venda.volume_venda * venda.preco_litro
            taxa_pagamento = venda.tipo_pagamento.taxa / 100
            valor_liquido = valor_bruto - (valor_bruto * taxa_pagamento)
            faturamento_total += valor_liquido

        return faturamento_total

    def _calcular_despesa(self, mes, ano, posto_id):
        despesa_compras = self._calcular_despesa_compras(mes, ano, posto_id)
        total_taxas = self._calcular_total_taxas(posto_id)
        total_folha = self._calcular_total_folha(posto_id)
        total_custos = self._calcular_total_custos(posto_id)
    
        return despesa_compras + total_taxas + total_folha + total_custos

    def _calcular_despesa_compras(self, mes, ano, posto_id):
        compras = models.Compra.objects.filter(data_compra__year=ano, data_compra__month=mes, posto_id=posto_id)
        return sum(compra.volume_compra * compra.preco_litro for compra in compras)

    def _calcular_total_taxas(self, posto_id, faturamento_mensal):
        taxas = models.Taxas.objects.filter(posto_id=posto_id).first()
        if taxas:
            # Convertendo os valores de taxas para decimais (por exemplo, de 1 para 0.01)
            ibran_taxa = taxas.ibran / 100
            ibama_taxa = taxas.ibama / 100
            agefis_taxa = taxas.agefis / 100
            comissao_bandeira_taxa = taxas.comissao_bandeira / 100
            impostos_recolhidos_taxa = taxas.impostos_recolhidos / 100

            # Calculando cada taxa individualmente e somando
            total_taxas = (
                faturamento_mensal * ibran_taxa +
                faturamento_mensal * ibama_taxa +
                faturamento_mensal * agefis_taxa +
                faturamento_mensal * comissao_bandeira_taxa +
                faturamento_mensal * impostos_recolhidos_taxa
            )
            return total_taxas
        return 0

    def _calcular_total_folha(self, posto_id):
        funcionarios = models.Funcionario.objects.filter(posto_id=posto_id)
        return sum(funcionario.total_folha for funcionario in funcionarios)

    def _calcular_total_custos(self, posto_id):
        custos = models.Custos.objects.filter(posto_id=posto_id).first()
        return sum([getattr(custos, field.name) for field in custos._meta.fields if field.name not in ['id', 'posto', 'posto_id']]) if custos else 0


class ResponsavelViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
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
        
    @action(detail=True, methods=['get'])
    def dadosPerfil(self, request, pk=None):
        try:
            posto = models.Posto.objects.get(pk=pk)
            responsavel = models.Responsavel.objects.filter(posto=posto).first()
            if responsavel:
                serializer_instance = serializer.ResponsavelComPostoSerializer(responsavel)
                return Response(serializer_instance.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Responsável não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except models.Posto.DoesNotExist:
            return Response({'message': 'Posto não encontrado'}, status=status.HTTP_404_NOT_FOUND)


class TaxasViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
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
        
    @action(detail=True, methods=['get'])
    def taxasPorPosto(self, request, pk=None):
        taxas = models.Taxas.objects.filter(posto_id=pk)
        serializer = TaxasSerializer(taxas, many=True)
        return Response(serializer.data)