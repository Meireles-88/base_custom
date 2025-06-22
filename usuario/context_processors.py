# usuario/context_processors.py
import re
from django.http import HttpRequest
from django.urls import resolve

def set_page_title(request: HttpRequest):
    try:
        current_url = resolve(request.path)
        if current_url.url_name == 'dashboard':
            return {'current_page_title': 'Dashboard'}
        elif current_url.url_name == 'user_list':
            return {'current_page_title': 'Lista de Usuários'}
        elif current_url.url_name == 'user_profile':
            from .models import UserProfile
            try:
                pk = int(request.path.split('/')[-2])
                profile = UserProfile.objects.get(pk=pk)
                return {'current_page_title': f'Perfil de {profile.user.username}'}
            except (UserProfile.DoesNotExist, ValueError):
                return {'current_page_title': 'Perfil de Usuário'}
        elif request.path == '/':
            return {'current_page_title': 'Página Inicial'}
    except Exception as e:
        print(f"Erro no contexto processador: {e}")  # Depuração
        return {'current_page_title': 'Dashboard'}  # Fallback