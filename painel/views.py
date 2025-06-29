# painel/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from instituicao.models import Instituicao

def home(request):
    """
    View para a página inicial pública do site.
    """
    return render(request, 'public/home.html')

@login_required
def dashboard(request):
    """
    Esta view agora funciona como o "Lobby" do usuário, renderizando
    o template a partir do seu novo caminho correto.
    """
    if request.user.is_superuser:
        # O Admin SI vê todas as instituições para poder gerenciá-las
        instituicoes_vinculadas = Instituicao.objects.all()
    else:
        # Um usuário comum (futuramente) verá apenas as instituições às quais tem vínculo
        try:
            instituicoes_vinculadas = Instituicao.objects.filter(userprofile=request.user.userprofile)
        except: # Captura o caso de não ter perfil ainda
            instituicoes_vinculadas = []


    context = {
        'instituicoes_vinculadas': instituicoes_vinculadas
    }
    # --- CORREÇÃO AQUI ---
    # O caminho do template foi atualizado para o local correto.
    return render(request, 'painel/dashboard.html', context)