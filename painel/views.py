# painel/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    """
    View para a página inicial pública do site.
    Utiliza o template base da área pública.
    """
    return render(request, 'public/home.html')

@login_required
def dashboard(request):
    """
    View para o painel inicial do usuário logado.
    Requer que o usuário esteja autenticado.
    Utiliza o template base da área logada.
    """
    return render(request, 'logged_in/dashboard.html')