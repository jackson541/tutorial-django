from django.http import HttpResponse
from django.shortcuts import render


class Carro:
    def __init__(self, nome, marca, cor):
        self.nome = nome
        self.marca = marca
        self.cor = cor

def cadastro_leitores(request):
    sistema_atual = 'Outro nome do sistema'

    carro = Carro('fusca', 'Volkswagen', 'azul')

    carros_nomes = ['fusca', 'hb20', 'honda fit']

    ano_lancamento_carros = {
        'fusca': 1959,
        'hb20': 2012,
        'honda_fit': 2003
    }

    context = {
        'nome_sistema': sistema_atual,
        'carro': carro,
        'carros_nomes': carros_nomes,
        'ano_lancamento_carros': ano_lancamento_carros
    }

    return render(request, 'leitores_cadastro.html', context)


