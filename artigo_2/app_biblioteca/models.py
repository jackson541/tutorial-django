from django.db import models


class Carro(models.Model):
    cor = models.CharField(max_length=100)
    velocidade_maxima = models.IntegerField()
    data_lancamento = models.DateField()

