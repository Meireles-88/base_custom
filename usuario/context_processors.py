# usuario/context_processors.py
from django.http import HttpRequest
from django.urls import resolve, reverse, NoReverseMatch
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from .models import UserProfile

def set_breadcrumb(request: HttpRequest):
    breadcrumb = []
    User = get_user_model()

    # Determina a página inicial dinamicamente
    if request.user.is_authenticated:
        breadcrumb.append({'title': 'Dashboard', 'url': reverse('painel:dashboard')})
    else:
        breadcrumb.append({'title': 'Início', 'url': reverse('painel:home')})

    try:
        current_url = resolve(request.path)
        print(f"Path: {request.path}, URL Name: {current_url.url_name}, Namespace: {current_url.namespace}, View: {current_url.func}")  # Depuração
        template_name = request.resolver_match.route  # Tenta inferir o template via rota

        # Mapeamento de url_name para títulos
        title_map = {
            'dashboard': 'Dashboard',
            'user_list': 'Lista de Usuários',
            'user_profile': 'Perfil de Usuário',
        }

        if current_url.url_name in title_map:
            if current_url.url_name == 'user_profile':
                breadcrumb.append({'title': 'Lista de Usuários', 'url': reverse('usuario:user_list')})
                pk = int(request.path.split('/')[-2])
                profile = UserProfile.objects.get(pk=pk)
                breadcrumb.append({'title': f'Perfil de {profile.user.username}', 'url': reverse('usuario:user_profile', args=[pk])})
            else:
                current_title = title_map.get(current_url.url_name)
                if current_title and current_url.url_name != 'dashboard':  # Evita duplicação
                    breadcrumb.append({'title': current_title, 'url': request.path})
        elif request.path == '/':
            breadcrumb[-1]['title'] = 'Página Inicial'  # Ajusta o título inicial para não autenticados
    except (NoReverseMatch, Exception) as e:
        print(f"Erro no breadcrumb: {e}, Path: {request.path}")

    return {'breadcrumb': breadcrumb}