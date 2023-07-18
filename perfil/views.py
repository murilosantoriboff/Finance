from django.shortcuts import render, redirect
from .models import Conta, Categoria
from django.contrib.messages import constants
from django.contrib import messages
from django.http import HttpResponse
from .utils import calcula_total
from django.db.models import Sum
from extrato.models import Valores

def home(request):
    contas = Conta.objects.all()
    total = calcula_total(contas, 'valor')
    return render(request, 'home.html', {'contas':contas, 'total': total})

def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    total = calcula_total(contas, 'valor')
    return render(request, 'gerenciar.html', {'contas':contas, 'total_conta': total, 'categorias':categorias})

def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')
    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Não existem dados o suficiente no formulario')
        return redirect('/perfil/gerenciar/')
    conta = Conta(apelido=apelido, banco=banco, tipo=tipo, valor=valor, icone=icone)
    conta.save()
    messages.add_message(request, constants.SUCCESS, 'Conta criada com sucesso')
    return redirect('/perfil/gerenciar/')

def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()

    messages.add_message(request, constants.SUCCESS, 'Conta Removida com sucesso')
    return redirect('/perfil/gerenciar/')

def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    if len(nome.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Não existem dados o suficiente no formulario')
        return redirect('/perfil/gerenciar/')
    if isinstance(essencial, bool) == True:
        categoria = Categoria(
            categoria=nome,
            essencial=essencial
        )

        categoria.save()

        messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
        return redirect('/perfil/gerenciar/')
    else:
        messages.add_message(request, constants.ERROR, 'Não existem dados o suficiente no formulario')
        return redirect('/perfil/gerenciar/')
    
def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial
    categoria.save()
    return redirect('/perfil/gerenciar/')

def dashboard(request):
    dados = dict()
    categorias = Categoria.objects.all()
    for categoria in categorias:
        tot = 0
        valores = Valores.objects.filter(categoria=categoria)
        for v in valores:
            tot += v.valor
        dados[categoria.categoria] = tot
    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})