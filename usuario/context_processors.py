# usuario/context_processors.py
import re
from django.http import HttpRequest

def set_page_title(request: HttpRequest):
    path = request.path
    if path == '/dashboard/':
        return {'current_page_title': 'Dashboard'}
    elif path == '/usuario/':
        return {'current_page_title': 'Lista de Usuários'}
    elif re.match(r'/usuario/\d+/$', path):
        from .models import UserProfile
        try:
            pk = int(path.split('/')[-2])
            profile = UserProfile.objects.get(pk=pk)
            return {'current_page_title': f'Perfil de {profile.user.username}'}
        except (UserProfile.DoesNotExist, ValueError):
            return {'current_page_title': 'Perfil de Usuário'}
    return {'current_page_title': 'Dashboard'}