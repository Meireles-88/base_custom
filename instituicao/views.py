from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import Instituicao, TipoInstituicao, Estado, Municipio
from usuario.models import UserProfile
from .forms import TipoInstituicaoForm, InstituicaoForm

class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class InstituicaoAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        instituicao = get_object_or_404(Instituicao, pk=self.kwargs['pk'])
        return hasattr(self.request.user, 'userprofile') and self.request.user.userprofile.instituicao == instituicao and self.request.user.userprofile.is_admin_instituicao

class InstituicaoListView(SuperuserRequiredMixin, ListView):
    model = Instituicao
    template_name = 'instituicao/lista_instituicoes.html'
    context_object_name = 'instituicoes'
    paginate_by = 10

class InstituicaoCreateView(SuperuserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Instituicao
    form_class = InstituicaoForm
    template_name = 'instituicao/instituicao_form.html'
    success_url = reverse_lazy('instituicao:lista_instituicoes')
    success_message = "Instituição criada com sucesso!"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.POST and 'estado' in self.request.POST:
            try:
                estado_id = int(self.request.POST.get('estado'))
                form.fields['municipio'].queryset = Municipio.objects.filter(estado_id=estado_id).order_by('nome')
            except (ValueError, TypeError): pass
        return form
    
    # --- MÉTODO ADICIONADO ---
    def form_invalid(self, form):
        # Se o formulário for inválido, adiciona uma mensagem de erro genérica.
        messages.error(self.request, "Não foi possível salvar a instituição. Por favor, corrija os erros abaixo.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Adicionar Nova Instituição'
        context['estados'] = Estado.objects.all()
        return context

class InstituicaoUpdateView(SuperuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Instituicao
    form_class = InstituicaoForm
    template_name = 'instituicao/instituicao_form.html'
    success_url = reverse_lazy('instituicao:lista_instituicoes')
    success_message = "Instituição atualizada com sucesso!"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.method == 'GET' and self.object.municipio:
            form.fields['municipio'].queryset = Municipio.objects.filter(estado=self.object.municipio.estado).order_by('nome')
        elif self.request.POST and 'estado' in self.request.POST:
            try:
                estado_id = int(self.request.POST.get('estado'))
                form.fields['municipio'].queryset = Municipio.objects.filter(estado_id=estado_id).order_by('nome')
            except (ValueError, TypeError): pass
        return form
        
    def form_invalid(self, form):
        messages.error(self.request, "Não foi possível atualizar a instituição. Por favor, corrija os erros abaixo.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Editar Instituição'
        context['estados'] = Estado.objects.all()
        if self.object.municipio:
            context['selected_estado_id'] = self.object.municipio.estado.id
        return context

class InstituicaoDeleteView(SuperuserRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Instituicao
    template_name = 'instituicao/instituicao_confirm_delete.html'
    success_url = reverse_lazy('instituicao:lista_instituicoes')
    success_message = "Instituição excluída com sucesso!"

class InstituicaoDetailView(InstituicaoAdminRequiredMixin, DetailView):
    model = Instituicao
    template_name = 'instituicao/detalhe_instituicao.html'
    context_object_name = 'instituicao'

class InstituicaoMembrosListView(InstituicaoAdminRequiredMixin, ListView):
    template_name = 'instituicao/membros_lista.html'
    context_object_name = 'membros'
    paginate_by = 20
    def get_queryset(self):
        self.instituicao = get_object_or_404(Instituicao, pk=self.kwargs['pk'])
        return UserProfile.objects.filter(instituicao=self.instituicao).select_related('user', 'cargo', 'patente').order_by('user__username')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instituicao'] = self.instituicao
        return context

@login_required
def carregar_municipios(request):
    estado_id = request.GET.get('estado_id')
    municipios = Municipio.objects.filter(estado_id=estado_id).order_by('nome')
    return JsonResponse(list(municipios.values('id', 'nome')), safe=False)

class TipoInstituicaoListView(SuperuserRequiredMixin, FormMixin, ListView):
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
            primeiro_erro = next(iter(form.errors.values()))[0]
            messages.error(self.request, f"Erro ao adicionar: {primeiro_erro}")
            return self.form_invalid(form)

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