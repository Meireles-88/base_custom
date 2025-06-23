# instituicao/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Instituicao

@login_required
def lista_instituicoes(request):
    """
    View para listar todas as instituições cadastradas.
    """
    instituicoes = Instituicao.objects.all()
    context = {
        'instituicoes': instituicoes
    }
    return render(request, 'instituicao/lista.html', context)