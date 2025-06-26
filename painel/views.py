from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from instituicao.models import Instituicao
from usuario.models import UserProfile

# --- Funções de Coleta de Dados para os Dashboards ---

def get_dashboard_data_admin_si():
    """ Coleta os dados para o dashboard do Super Admin (Nível SI). """
    total_instituicoes = Instituicao.objects.count()
    total_usuarios = User.objects.count()
    # Adicione outras métricas globais que desejar aqui...
    context = {
        'total_instituicoes': total_instituicoes,
        'total_usuarios': total_usuarios,
    }
    return context

def get_dashboard_data_admin_institucional(instituicao):
    """ Coleta os dados para o dashboard do Admin Institucional. """
    # Filtra os membros apenas da instituição do admin logado
    membros = UserProfile.objects.filter(instituicao=instituicao)
    total_membros = membros.count()
    admins_locais = membros.filter(is_admin_instituicao=True).count()
    # Adicione outras métricas da instituição aqui...
    context = {
        'instituicao': instituicao,
        'total_membros': total_membros,
        'admins_locais': admins_locais,
    }
    return context

def get_dashboard_data_agente(profile):
    """ Coleta os dados para o dashboard de um usuário comum (agente). """
    # Adicione métricas específicas do agente aqui...
    context = {
        'instituicao': profile.instituicao,
    }
    return context

# --- Views Principais ---

def home(request):
    """ View para a página inicial pública do site. """
    return render(request, 'public/home.html')

@login_required
def dashboard(request):
    """
    View principal do Dashboard que renderiza o painel correto
    de acordo com o nível de permissão do usuário.
    """
    # Garante que o perfil do usuário seja carregado para evitar erros
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Lida com o caso raro de um usuário não ter perfil, talvez redirecionando
        # ou mostrando uma mensagem de erro. Por agora, tratamos como usuário comum.
        user_profile = None

    if request.user.is_superuser:
        context = get_dashboard_data_admin_si()
        return render(request, 'logged_in/dashboards/admin_si.html', context)

    # Verifica se o usuário tem perfil e se é admin da instituição
    elif user_profile and user_profile.is_admin_instituicao:
        context = get_dashboard_data_admin_institucional(user_profile.instituicao)
        return render(request, 'logged_in/dashboards/admin_institucional.html', context)
        
    else:
        context = get_dashboard_data_agente(user_profile)
        return render(request, 'logged_in/dashboards/agente.html', context)