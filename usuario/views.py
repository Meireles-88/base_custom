# usuario/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
def user_list(request):
    """
    Exibe a lista de perfis de usuários, incluindo aqueles sem UserProfile.
    """
    User = get_user_model()
    users = User.objects.all()  # Inclui todos os usuários
    profiles = {profile.user_id: profile for profile in UserProfile.objects.all()}  # Mapeia perfis por user_id
    return render(request, 'usuario/user_list.html', {'users': users, 'profiles': profiles})

@login_required
def user_profile(request, pk):
    """
    Exibe os detalhes de um perfil de usuário específico, incluindo cidade/UF, e-mail, CPF, celular, telefone e foto.
    """
    profile = get_object_or_404(UserProfile, pk=pk)
    return render(request, 'usuario/user_profile.html', {'profile': profile})

@login_required
@permission_required('usuario.can_change_userprofile', raise_exception=True)
def user_edit(request, pk):
    """
    Permite a edição de um perfil de usuário específico.
    """
    profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)  # Adicionei request.FILES para foto
        if form.is_valid():
            form.save()
            messages.success(request, f'Perfil de {profile.user.username} atualizado com sucesso!')
            return redirect('usuario:user_profile', pk=pk)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'usuario/user_edit.html', {'form': form, 'profile': profile})

@login_required
@permission_required('usuario.can_add_userprofile', raise_exception=True)
def user_create(request):
    """
    Permite criar um novo perfil de usuário.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)  # Adicionei request.FILES para foto
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Vincula ao usuário atual (ajustável para admin criar outros)
            profile.save()
            messages.success(request, f'Perfil de {profile.user.username} criado com sucesso!')
            return redirect('usuario:user_list')
    else:
        form = UserProfileForm()
    return render(request, 'usuario/user_create.html', {'form': form})

@login_required
@permission_required('usuario.can_delete_userprofile', raise_exception=True)
def user_delete(request, pk):
    """
    Permite excluir um perfil de usuário e o usuário associado.
    """
    profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'POST':
        user = profile.user
        profile.delete()
        user.delete()  # Remove o usuário associado
        messages.success(request, f'Perfil e usuário {user.username} excluídos com sucesso!')
        return redirect('usuario:user_list')
    return render(request, 'usuario/user_delete.html', {'profile': profile})

@login_required
@permission_required('usuario.can_change_userprofile', raise_exception=True)
@require_POST
def update_status(request, pk):
    """
    Atualiza o status (ativo/inativo) de um perfil de usuário via requisição AJAX.
    """
    profile = get_object_or_404(UserProfile, pk=pk)
    ativo = request.POST.get('ativo') == 'True'
    profile.ativo = ativo
    profile.save()
    return JsonResponse({'success': True})

# Formulário para validação
from django import forms

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['cargo', 'instituicao', 'cidade_uf', 'email', 'cpf', 'celular', 'fone', 'foto', 'ativo']