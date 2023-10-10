from rest_framework import serializers
from TankSaverAPI import models


class PostoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Posto
        fields = '__all__'

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Funcionario
        fields = '__all__'

class CustosSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Custos
        fields = '__all__'

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Compra
        fields = '__all__'

class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Venda
        fields = '__all__'
        
class TipoCombustivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoCombustivel
        fields = '__all__'

class TipoDePagamentoSerealizer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoPagamento
        fields = '__all__'
        
class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Historico
        fields = '__all__'
        
class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Responsavel
        fields = '__all__'

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Endereco
        fields = '__all__'

class TaxasSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Taxas
        fields = '__all__'