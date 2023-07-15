from django.db import models
from datetime import datetime
from perfil.utils import calcula_total

class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.categoria
    
    def total_gasto(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(categoria__id=self.id).filter(data__month=datetime.now().month).filter(tipo='S')
        tot = calcula_total(valores, 'valor')
        return tot
    
    def calcula_percentual_gasto_por_categoria(self):
        """
        valor_planejamento ------- 100%
        total_gasto -------------- x

        """
        try:
            return int(self.total_gasto() * 100 / self.valor_planejamento)
        except:
            return 0

class Conta(models.Model):
    banco_choices = (
        ('NU', 'Nubank'),
        ('CE','Caixa Economica'),
        ('BR','Bradesco'),
        ('BC','Banco do Brasil')
    )
    tipo_choices = (
        ('pf', 'Pessoa Fisica'),
        ('pj', 'Pessoa Juridica')
    )

    apelido = models.CharField(max_length=100)
    banco = models.CharField(max_length=2, choices=banco_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to='icones')

    def __str__(self) -> str:
        return self.apelido