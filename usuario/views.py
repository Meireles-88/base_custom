from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

# Importações de modelos e formulários
from .models import UserProfile, Cargo, Patente, Funcao
from .forms import AdminUserCreationForm, UserProfileEditForm, CargoForm, PatenteForm, FuncaoForm
# Importando o Mixin de permissão do app 'instituicao' para reutilização
from instituicao.mixins import SuperuserRequiredMixin

# --- Views de Gerenciamento de Usuários (para Admin SI) ---

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


# --- PAINEL DE ADMINISTRAÇÃO SI ---
class AdministracaoSIView(SuperuserRequiredMixin, ListView):
    """ View para a página central de administração do Nível SI. """
    template_name = 'usuario/administracao/painel_admin_si.html'
    def get_queryset(self):
        # Esta view não exibe uma lista, apenas serve como um hub de links.
        return []

# --- CRUD PARA CARGOS ---
class CargoListView(SuperuserRequiredMixin, ListView):
    model = Cargo
    template_name = 'partials/generic_list.html'
    context_object_name = 'itens'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'titulo': "Cargos Globais", 'url_novo': 'usuario:cria_cargo', 'url_edicao': 'usuario:edita_cargo', 'url_exclusao': 'usuario:exclui_cargo'})
        return context

class CargoCreateView(SuperuserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'partials/generic_form.html'
    success_url = reverse_lazy('usuario:lista_cargos')
    success_message = "Cargo criado com sucesso!"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Adicionar Novo Cargo Global'
        return context

class CargoUpdateView(SuperuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'partials/generic_form.html'
    success_url = reverse_lazy('usuario:lista_cargos')
    success_message = "Cargo atualizado com sucesso!"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Editar Cargo Global'
        return context

class CargoDeleteView(SuperuserRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Cargo
    template_name = 'partials/generic_confirm_delete.html'
    success_url = reverse_lazy('usuario:lista_cargos')
    success_message = "Cargo excluído com sucesso!"


# --- CRUD PARA PATENTES ---
class PatenteListView(SuperuserRequiredMixin, ListView):
    model = Patente
    template_name = 'partials/generic_list.html'
    context_object_name = 'itens'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'titulo': "Patentes", 'url_novo': 'usuario:cria_patente', 'url_edicao': 'usuario:edita_patente', 'url_exclusao': 'usuario:exclui_patente'})
        return context

class PatenteCreateView(SuperuserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Patente
    form_class = PatenteForm
    template_name = 'partials/generic_form.html'
    success_url = reverse_lazy('usuario:lista_patentes')
    success_message = "Patente criada com sucesso!"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Adicionar Nova Patente'
        return context

class PatenteUpdateView(SuperuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Patente
    form_class = PatenteForm
    template_name = 'partials/generic_form.html'
    success_url = reverse_lazy('usuario:lista_patentes')
    success_message = "Patente atualizada com sucesso!"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Editar Patente'
        return context

class PatenteDeleteView(SuperuserRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Patente
    template_name = 'partials/generic_confirm_delete.html'
    success_url = reverse_lazy('usuario:lista_patentes')
    success_message = "Patente excluída com sucesso!"


# --- CRUD PARA FUNÇÕES ---
class FuncaoListView(SuperuserRequiredMixin, ListView):
    model = Funcao
    template_name = 'partials/generic_list.html'
    context_object_name = 'itens'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'titulo': "Funções", 'url_novo': 'usuario:cria_funcao', 'url_edicao': 'usuario:edita_funcao', 'url_exclusao': 'usuario:exclui_funcao'})
        return context

class FuncaoCreateView(SuperuserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Funcao
    form_class = FuncaoForm
    template_name = 'partials/generic_form.html'
    success_url = reverse_lazy('usuario:lista_funcoes')
    success_message = "Função criada com sucesso!"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Adicionar Nova Função'
        return context

class FuncaoUpdateView(SuperuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Funcao
    form_class = FuncaoForm
    template_name = 'partials/generic_form.html'
    success_url = reverse_lazy('usuario:lista_funcoes')
    success_message = "Função atualizada com sucesso!"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Editar Função'
        return context

class FuncaoDeleteView(SuperuserRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Funcao
    template_name = 'partials/generic_confirm_delete.html'
    success_url = reverse_lazy('usuario:lista_funcoes')
    success_message = "Função excluída com sucesso!"