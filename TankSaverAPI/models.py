from django.core.exceptions import ValidationError
from django.db import models
from validate_docbr import CPF, CNPJ

#Funções para inserções inválidas

def valida_cnpj(cnpj):
    cnpj_validator = CNPJ()
    if not cnpj_validator.validate(cnpj):
        raise ValidationError(f"{cnpj} não é um CNPJ válido.")

def valida_cpf(cpf):
    cpf_validator = CPF()
    if not cpf_validator.validate(cpf):
        raise ValidationError(f"{cpf} não é um CPF válido.")

#Tabelas do DB ===========================================================

class TipoCombustivel(models.Model):
    tipo_combustivel = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.tipo_combustivel
    
    class Meta:
        db_table = 'tb_tipo_combustivel'


class Responsavel(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, validators=[valida_cpf])
    email = models.EmailField(max_length=100)
    telefone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = 'tb_responsavel'
    

class Endereco(models.Model):
    endereco = models.CharField(max_length=150)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    
    def __str__(self):
        return self.endereco
    
    class Meta:
        db_table = 'tb_endereco'

       
class Posto(models.Model):
    nome_fantasia = models.CharField(max_length=100)
    bandeira = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, validators=[valida_cnpj])
    email = models.EmailField(max_length=100)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.PROTECT)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT)
    senha = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nome_fantasia
    
    class Meta:
        db_table = 'tb_posto'


class TipoPagamento(models.Model):
    tipo_pagamento = models.CharField(max_length=20, unique=True)
    taxa = models.DecimalField(max_digits=5, decimal_places=2)
    posto = models.ForeignKey(Posto, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.tipo_pagamento

    class Meta:
        db_table = 'tb_tipo_pagamento'


class Taxas(models.Model):
    ibran = models.DecimalField(max_digits=15, decimal_places=2)
    ibama = models.DecimalField(max_digits=15, decimal_places=2)
    agefis = models.DecimalField(max_digits=15, decimal_places=2)
    comissao_bandeira = models.DecimalField(max_digits=15, decimal_places=2)
    impostos_recolhidos = models.DecimalField(max_digits=15, decimal_places=2)
    posto = models.ForeignKey(Posto, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.posto
    
    class Meta:
        db_table = 'tb_taxas'


class Custos(models.Model):
    iptu = models.DecimalField(max_digits=15, decimal_places=2)
    custos_operacionais = models.DecimalField(max_digits=15, decimal_places=2)
    honorarios_contabeis = models.DecimalField(max_digits=15, decimal_places=2)
    telefone_internet = models.DecimalField(max_digits=15, decimal_places=2)
    luz = models.DecimalField(max_digits=15, decimal_places=2)
    agua = models.DecimalField(max_digits=15, decimal_places=2)
    softwares = models.DecimalField(max_digits=15, decimal_places=2)
    posto = models.ForeignKey(Posto, on_delete=models.PROTECT)

    class Meta:
        db_table = 'tb_custos'


class Compra(models.Model):
    tipo_combustivel = models.ForeignKey(TipoCombustivel, on_delete=models.PROTECT)
    volume_compra = models.DecimalField(max_digits=8, decimal_places=2)
    preco_litro = models.DecimalField(max_digits=6, decimal_places=2)
    data_compra = models.DateField()
    posto = models.ForeignKey(Posto, on_delete=models.PROTECT)
    

    class Meta:
        db_table = 'tb_compra'


class Venda(models.Model):
    tipo_pagamento = models.ForeignKey(TipoPagamento, on_delete=models.PROTECT)
    tipo_combustivel = models.ForeignKey(TipoCombustivel, on_delete=models.PROTECT)
    volume_venda = models.DecimalField(max_digits=15, decimal_places=2)
    preco_litro = models.DecimalField(max_digits=15, decimal_places=2)
    posto = models.ForeignKey(Posto, on_delete=models.PROTECT)
    data_venda = models.DateField()

    class Meta:
        db_table = 'tb_venda'

   
class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    total_folha = models.DecimalField(max_digits=15, decimal_places=2)
    posto = models.ForeignKey(Posto, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = 'tb_funcionario'


class Historico(models.Model):
    posto = models.ForeignKey(Posto, on_delete=models.PROTECT)
    despesa_mensal = models.DecimalField(max_digits=15, decimal_places=2)
    faturamento_mensal = models.DecimalField(max_digits=15, decimal_places=2)
    total_rendimento = models.DecimalField(max_digits=15, decimal_places=2)
    data_historico = models.DateField()
    
    class Meta:
        db_table = 'tb_historico'