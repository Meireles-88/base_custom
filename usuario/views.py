from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from .models import UserProfile, Cargo, Patente, Funcao
from .forms import AdminUserCreationForm, UserProfileEditForm, CargoForm, PatenteForm, FuncaoForm
from instituicao.views import SuperuserRequiredMixin # Reutilizando nosso Mixin

# --- VIEWS DE GERENCIAMENTO DE USUÁRIOS (Existentes) ---
@login_required
def user_list(request):
    #...
    pass

@login_required
def user_create(request):
    #...
    pass

@login_required
def user_profile(request, pk):
    #...
    pass

@login_required
def user_edit(request, pk):
    #...
    pass

@login_required
def user_delete(request, pk):
    #...
    pass


# --- VIEWS PARA O PAINEL DE ADMINISTRAÇÃO SI ---

class AdministracaoListView(SuperuserRequiredMixin, ListView):
    """ Uma view simples para a página central de administração. """
    template_name = 'usuario/administracao/painel_admin.html'
    # Esta view não precisa de um modelo, pois é apenas um hub de links.
    def get_queryset(self):
        return []

# --- VIEWS PARA GERENCIAR CARGOS ---
class CargoListView(SuperuserRequiredMixin, ListView):
    model = Cargo
    template_name = 'usuario/administracao/generic_list.html'
    context_object_name = 'itens'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Cargos"
        context['url_novo'] = 'usuario:cria_cargo'
        return context

class CargoCreateView(SuperuserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'usuario/administracao/generic_form.html'
    success_url = reverse_lazy('usuario:lista_cargos')
    success_message = "Cargo criado com sucesso!"

class CargoUpdateView(SuperuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'usuario/administracao/generic_form.html'
    success_url = reverse_lazy('usuario:lista_cargos')
    success_message = "Cargo atualizado com sucesso!"

class CargoDeleteView(SuperuserRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Cargo
    template_name = 'usuario/administracao/generic_confirm_delete.html'
    success_url = reverse_lazy('usuario:lista_cargos')
    success_message = "Cargo excluído com sucesso!"

# --- VIEWS PARA GERENCIAR PATENTES ---
class PatenteListView(SuperuserRequiredMixin, ListView):
    model = Patente
    template_name = 'usuario/administracao/generic_list.html'
    context_object_name = 'itens'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Patentes"
        context['url_novo'] = 'usuario:cria_patente'
        return context

class PatenteCreateView(SuperuserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Patente
    form_class = PatenteForm
    template_name = 'usuario/administracao/generic_form.html'
    success_url = reverse_lazy('usuario:lista_patentes')
    success_message = "Patente criada com sucesso!"

class PatenteUpdateView(SuperuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Patente
    form_class = PatenteForm
    template_name = 'usuario/administracao/generic_form.html'
    success_url = reverse_lazy('usuario:lista_patentes')
    success_message = "Patente atualizada com sucesso!"

class PatenteDeleteView(SuperuserRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Patente
    template_name = 'usuario/administracao/generic_confirm_delete.html'
    success_url = reverse_lazy('usuario:lista_patentes')
    success_message = "Patente excluída com sucesso!"

# --- VIEWS PARA GERENCIAR FUNÇÕES ---
class FuncaoListView(SuperuserRequiredMixin, ListView):
    model = Funcao
    template_name = 'usuario/administracao/generic_list.html'
    context_object_name = 'itens'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Funções"
        context['url_novo'] = 'usuario:cria_funcao'
        return context

class FuncaoCreateView(SuperuserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Funcao
    form_class = FuncaoForm
    template_name = 'usuario/administracao/generic_form.html'
    success_url = reverse_lazy('usuario:lista_funcoes')
    success_message = "Função criada com sucesso!"

class FuncaoUpdateView(SuperuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Funcao
    form_class = FuncaoForm
    template_name = 'usuario/administracao/generic_form.html'
    success_url = reverse_lazy('usuario:lista_funcoes')
    success_message = "Função atualizada com sucesso!"

class FuncaoDeleteView(SuperuserRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Funcao
    template_name = 'usuario/administracao/generic_confirm_delete.html'
    success_url = reverse_lazy('usuario:lista_funcoes')
    success_message = "Função excluída com sucesso!"