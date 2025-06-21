# usuario/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def user_list(request):
    """
    Exibe a lista de perfis de usuários.
    """
    profiles = UserProfile.objects.all()
    return render(request, 'usuario/user_list.html', {'profiles': profiles})

@login_required
def user_profile(request, pk):
    """
    Exibe os detalhes de um perfil de usuário específico.
    """
    profile = get_object_or_404(UserProfile, pk=pk)
    return render(request, 'usuario/user_profile.html', {'profile': profile})