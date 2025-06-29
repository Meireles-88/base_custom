# usuario/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.views.generic import ListView
from .models import UserProfile
from .forms import AdminUserCreationForm, UserProfileEditForm
from instituicao.mixins import SuperuserRequiredMixin

@login_required
def user_list(request):
    """ Exibe a lista de todos os perfis de usuários do sistema. """
    all_profiles = UserProfile.objects.select_related('user', 'instituicao', 'cargo', 'patente').all()
    context = {'profiles': all_profiles}
    return render(request, 'usuario/user_list.html', context)

@login_required
def user_create(request):
    """ Permite que o Admin SI crie um novo usuário e seu perfil completo. """
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para realizar esta ação.")
        return redirect('painel:dashboard')
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo usuário criado com sucesso!')
            return redirect('usuario:user_list')
        else:
            messages.error(request, 'Erro ao criar o usuário. Verifique os dados.')
    else:
        form = AdminUserCreationForm()
    context = {'form': form, 'titulo_pagina': 'Adicionar Novo Usuário (Admin SI)'}
    return render(request, 'usuario/user_form.html', context)

@login_required
def user_profile(request, pk):
    """ Exibe os detalhes de um perfil de usuário específico. """
    profile = get_object_or_404(UserProfile.objects.select_related('user'), pk=pk)
    return render(request, 'usuario/user_profile.html', {'profile': profile})

@login_required
def user_edit(request, pk):
    """ Permite que o Admin SI edite os dados de um usuário. """
    profile = get_object_or_404(UserProfile, pk=pk)
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para realizar esta ação.")
        return redirect('usuario:user_list')
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Perfil de {profile.user.username} atualizado com sucesso!')
            return redirect('usuario:user_profile', pk=profile.pk)
        else:
            messages.error(request, 'Erro ao atualizar o perfil. Verifique os dados.')
    else:
        form = UserProfileEditForm(instance=profile)
    context = {'form': form, 'titulo_pagina': f'Editar Perfil de {profile.user.username}'}
    return render(request, 'usuario/user_form.html', context)

@login_required
@transaction.atomic
def user_delete(request, pk):
    """ Exclui um usuário e seu perfil associado. """
    profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'POST':
        user_to_delete = profile.user
        if user_to_delete:
            user_username = user_to_delete.username
            user_to_delete.delete()
            messages.success(request, f'Usuário {user_username} e seu perfil foram excluídos com sucesso!')
        else:
            profile.delete()
            messages.success(request, 'Perfil sem usuário associado foi excluído com sucesso!')
        return redirect('usuario:user_list')
    return render(request, 'usuario/user_delete.html', {'profile': profile})

@login_required
def user_list(request):
    all_profiles = UserProfile.objects.select_related('user', 'instituicao', 'cargo', 'patente').all()
    context = {'profiles': all_profiles}
    return render(request, 'usuario/user_list.html', context)

# --- PAINEL DE ADMINISTRAÇÃO SI ---
class AdministracaoSIView(SuperuserRequiredMixin, ListView):
    """ View para a página central de administração do Nível SI. """
    template_name = 'usuario/administracao/painel_admin_si.html'
    def get_queryset(self):
        # Esta view não exibe uma lista, apenas serve como um hub de links.
        return []