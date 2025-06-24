from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import Instituicao, TipoInstituicao
from .forms import TipoInstituicaoForm, InstituicaoForm # Supondo que InstituicaoForm já existe em forms.py

# --- Mixin de Segurança (Mantido) ---
class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Garante que o usuário logado seja um superusuário.
    """
    def test_func(self):
        return self.request.user.is_superuser

# --- Views para gerenciar Instituições ---

class InstituicaoListView(SuperuserRequiredMixin, ListView):
    """
    View principal para listar as Instituições.
    (Substitui a antiga função 'lista_instituicoes')
    """
    model = Instituicao
    template_name = 'instituicao/lista_instituicoes.html'
    context_object_name = 'instituicoes'
    paginate_by = 10


# --- Views do CRUD para Tipo de Instituição (Otimizado) ---

class TipoInstituicaoListView(SuperuserRequiredMixin, FormMixin, ListView):
    """
    Lista os Tipos de Instituição e permite a criação in-line.
    """
    model = TipoInstituicao
    template_name = 'instituicao/tipo/lista.html'
    context_object_name = 'tipos'
    paginate_by = 10
    form_class = TipoInstituicaoForm
    success_url = reverse_lazy('instituicao:lista_tipos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(self.request, "Novo tipo de instituição adicionado com sucesso!")
            return self.form_valid(form)
        else:
            # Pega o primeiro erro do formulário para exibir uma mensagem mais específica
            primeiro_erro = next(iter(form.errors.values()))[0]
            messages.error(self.request, f"Erro ao adicionar: {primeiro_erro}")
            return self.form_invalid(form)

# REMOVIDO: A view TipoInstituicaoCreateView não é mais necessária.

class TipoInstituicaoUpdateView(SuperuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TipoInstituicao
    form_class = TipoInstituicaoForm
    template_name = 'instituicao/tipo/form.html'
    success_url = reverse_lazy('instituicao:lista_tipos')
    success_message = "Tipo de instituição atualizado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Editar Tipo de Instituição'
        return context

class TipoInstituicaoDeleteView(SuperuserRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TipoInstituicao
    template_name = 'instituicao/tipo/confirm_delete.html'
    success_url = reverse_lazy('instituicao:lista_tipos')
    success_message = "Tipo de instituição excluído com sucesso!"