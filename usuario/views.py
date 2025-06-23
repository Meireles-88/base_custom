# usuario/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction # Importar transaction

from .models import UserProfile
from .forms import CustomUserCreationForm, UserProfileEditForm

@login_required
def user_list(request):
    """
    Exibe a lista de perfis de usuários de forma otimizada.
    """
    all_profiles = UserProfile.objects.select_related('user').all()
    context = {'profiles': all_profiles}
    return render(request, 'usuario/user_list.html', context)

@login_required
def user_profile(request, pk):
    """
    Exibe os detalhes de um perfil de usuário específico.
    """
    profile = get_object_or_404(UserProfile.objects.select_related('user'), pk=pk)
    return render(request, 'usuario/user_profile.html', {'profile': profile})

@login_required
#@permission_required('usuario.change_userprofile', raise_exception=True)
def user_edit(request, pk):
    """
    Permite a edição de um perfil de usuário usando o formulário UserProfileEditForm.
    """
    profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Perfil de {profile.user.username} atualizado com sucesso!')
            return redirect('usuario:user_profile', pk=pk)
        else:
            messages.error(request, 'Ocorreu um erro ao atualizar. Por favor, verifique os dados.')
    else:
        form = UserProfileEditForm(instance=profile)
        
    context = {'form': form, 'profile': profile}
    return render(request, 'usuario/user_edit.html', context)

@login_required
#@permission_required('usuario.add_userprofile', raise_exception=True)
def user_create(request):
    """
    Permite criar um novo usuário e seu perfil associado de uma só vez.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # @transaction.atomic garante que ou tudo é salvo (User e Perfil) ou nada é.
            with transaction.atomic():
                profile = form.save()
            messages.success(request, f'Usuário {profile.user.username} criado com sucesso!')
            return redirect('usuario:user_list')
        else:
            messages.error(request, 'Não foi possível criar o usuário. Por favor, verifique os dados.')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'usuario/user_create.html', {'form': form})

@login_required
#@permission_required('usuario.delete_userprofile', raise_exception=True)
@transaction.atomic # Garante a integridade da exclusão
def user_delete(request, pk):
    """
    Permite excluir um perfil de usuário e o usuário associado do sistema.
    """
    profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'POST':
        # É mais seguro obter o usuário do perfil e verificar se ele existe
        user_to_delete = profile.user
        if user_to_delete:
            user_username = user_to_delete.username
            user_to_delete.delete() # Deletar o usuário irá deletar o perfil em cascata
            messages.success(request, f'Usuário {user_username} e seu perfil foram excluídos com sucesso!')
        else:
            # Caso raro onde o perfil não tem um usuário associado
            profile.delete()
            messages.success(request, 'Perfil sem usuário associado foi excluído com sucesso!')

        return redirect('usuario:user_list')
        
    return render(request, 'usuario/user_delete.html', {'profile': profile})

@login_required
#@permission_required('usuario.change_userprofile', raise_exception=True)
@require_POST
def update_status(request, pk):
    """
    Atualiza o status (ativo/inativo) de um perfil de usuário via requisição AJAX.
    """
    profile = get_object_or_404(UserProfile, pk=pk)
    ativo_str = request.POST.get('ativo')
    
    if ativo_str not in ['true', 'false']:
        return JsonResponse({'success': False, 'error': 'Valor de status inválido'}, status=400)
        
    profile.ativo = (ativo_str == 'true')
    profile.save()
    return JsonResponse({'success': True})