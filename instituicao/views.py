from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect

# Importações de Modelos, Formulários e Mixins
from .models import Instituicao, TipoInstituicao, Estado, Municipio
from usuario.models import UserProfile, Cargo, Patente, Funcao
from .forms import InstituicaoForm, TipoInstituicaoForm
from usuario.forms import CargoForm, PatenteForm, FuncaoForm
from .mixins import SuperuserRequiredMixin, InstituicaoAdminRequiredMixin

# --- Views de Gerenciamento Geral de Instituições (para Admin SI) ---

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

    def form_invalid(self, form):
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
        context['titulo_pagina'] = f'Editar Instituição: {self.object.nome_gerado}'
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
    if not estado_id:
        return JsonResponse([], safe=False)
    municipios = Municipio.objects.filter(estado_id=estado_id).order_by('nome')
    return JsonResponse(list(municipios.values('id', 'nome')), safe=False)


# --- PAINEL DE GERENCIAMENTO INSTITUCIONAL ---
class GerenciarInstituicaoView(InstituicaoAdminRequiredMixin, DetailView):
    model = Instituicao
    template_name = 'instituicao/gerenciar/painel.html'
    context_object_name = 'instituicao'

# --- CLASSE BASE PARA AS VIEWS DE GERENCIAMENTO ---
class BaseGerenciarView(InstituicaoAdminRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.instituicao = get_object_or_404(Instituicao, pk=self.kwargs['instituicao_pk'])
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instituicao'] = self.instituicao
        return context

# --- CRUD COMPLETO PARA CARGOS ---
class CargoListView(BaseGerenciarView, ListView):
    model = Cargo
    template_name = 'partials/generic_list.html'
    context_object_name = 'itens'
    def get_queryset(self):
        return Cargo.objects.filter(instituicao=self.instituicao)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'titulo': "Cargos", 'url_novo': 'instituicao:cria_cargo', 'url_edicao': 'instituicao:edita_cargo', 'url_exclusao': 'instituicao:exclui_cargo'})
        return context

class CargoCreateView(BaseGerenciarView, SuccessMessageMixin, CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'partials/generic_form.html'
    success_message = "Cargo criado com sucesso!"
    def form_valid(self, form):
        form.instance.instituicao = self.instituicao
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('instituicao:gerenciar_cargos', kwargs={'instituicao_pk': self.instituicao.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Adicionar Novo Cargo'
        return context

class CargoUpdateView(BaseGerenciarView, SuccessMessageMixin, UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'partials/generic_form.html'
    success_message = "Cargo atualizado com sucesso!"
    def get_queryset(self): return Cargo.objects.filter(instituicao=self.instituicao)
    def get_success_url(self):
        return reverse_lazy('instituicao:gerenciar_cargos', kwargs={'instituicao_pk': self.instituicao.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = f"Editar Cargo: {self.object.nome}"
        return context

class CargoDeleteView(BaseGerenciarView, SuccessMessageMixin, DeleteView):
    model = Cargo
    template_name = 'partials/generic_confirm_delete.html'
    success_message = "Cargo excluído com sucesso!"
    def get_queryset(self): return Cargo.objects.filter(instituicao=self.instituicao)
    def get_success_url(self):
        return reverse_lazy('instituicao:gerenciar_cargos', kwargs={'instituicao_pk': self.instituicao.pk})

# --- CRUD COMPLETO PARA PATENTES ---
class PatenteListView(BaseGerenciarView, ListView):
    model = Patente
    template_name = 'partials/generic_list.html'
    context_object_name = 'itens'
    def get_queryset(self): return Patente.objects.filter(instituicao=self.instituicao)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'titulo': "Patentes", 'url_novo': 'instituicao:cria_patente', 'url_edicao': 'instituicao:edita_patente', 'url_exclusao': 'instituicao:exclui_patente'})
        return context

class PatenteCreateView(BaseGerenciarView, SuccessMessageMixin, CreateView):
    model = Patente
    form_class = PatenteForm
    template_name = 'partials/generic_form.html'
    success_message = "Patente criada com sucesso!"
    def form_valid(self, form):
        form.instance.instituicao = self.instituicao
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('instituicao:gerenciar_patentes', kwargs={'instituicao_pk': self.instituicao.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Adicionar Nova Patente'
        return context

class PatenteUpdateView(BaseGerenciarView, SuccessMessageMixin, UpdateView):
    model = Patente
    form_class = PatenteForm
    template_name = 'partials/generic_form.html'
    success_message = "Patente atualizada com sucesso!"
    def get_queryset(self): return Patente.objects.filter(instituicao=self.instituicao)
    def get_success_url(self):
        return reverse_lazy('instituicao:gerenciar_patentes', kwargs={'instituicao_pk': self.instituicao.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = f"Editar Patente: {self.object.nome}"
        return context

class PatenteDeleteView(BaseGerenciarView, SuccessMessageMixin, DeleteView):
    model = Patente
    template_name = 'partials/generic_confirm_delete.html'
    success_message = "Patente excluída com sucesso!"
    def get_queryset(self): return Patente.objects.filter(instituicao=self.instituicao)
    def get_success_url(self):
        return reverse_lazy('instituicao:gerenciar_patentes', kwargs={'instituicao_pk': self.instituicao.pk})

# --- CRUD COMPLETO PARA FUNÇÕES ---
class FuncaoListView(BaseGerenciarView, ListView):
    model = Funcao
    template_name = 'partials/generic_list.html'
    context_object_name = 'itens'
    def get_queryset(self): return Funcao.objects.filter(instituicao=self.instituicao)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'titulo': "Funções", 'url_novo': 'instituicao:cria_funcao', 'url_edicao': 'instituicao:edita_funcao', 'url_exclusao': 'instituicao:exclui_funcao'})
        return context

class FuncaoCreateView(BaseGerenciarView, SuccessMessageMixin, CreateView):
    model = Funcao
    form_class = FuncaoForm
    template_name = 'partials/generic_form.html'
    success_message = "Função criada com sucesso!"
    def form_valid(self, form):
        form.instance.instituicao = self.instituicao
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('instituicao:gerenciar_funcoes', kwargs={'instituicao_pk': self.instituicao.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Adicionar Nova Função'
        return context

class FuncaoUpdateView(BaseGerenciarView, SuccessMessageMixin, UpdateView):
    model = Funcao
    form_class = FuncaoForm
    template_name = 'partials/generic_form.html'
    success_message = "Função atualizada com sucesso!"
    def get_queryset(self): return Funcao.objects.filter(instituicao=self.instituicao)
    def get_success_url(self):
        return reverse_lazy('instituicao:gerenciar_funcoes', kwargs={'instituicao_pk': self.instituicao.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = f"Editar Função: {self.object.nome}"
        return context

class FuncaoDeleteView(BaseGerenciarView, SuccessMessageMixin, DeleteView):
    model = Funcao
    template_name = 'partials/generic_confirm_delete.html'
    success_message = "Função excluída com sucesso!"
    def get_queryset(self): return Funcao.objects.filter(instituicao=self.instituicao)
    def get_success_url(self):
        return reverse_lazy('instituicao:gerenciar_funcoes', kwargs={'instituicao_pk': self.instituicao.pk})


# --- Views de Tipo de Instituição (Global, para Admin SI) ---
class TipoInstituicaoView(SuperuserRequiredMixin, View):
    template_name = 'instituicao/tipo/lista.html'
    form_class = TipoInstituicaoForm
    def get(self, request, *args, **kwargs):
        tipos = TipoInstituicao.objects.all()
        form = self.form_class()
        context = {'tipos': tipos, 'form': form}
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Novo tipo de instituição adicionado com sucesso!")
            return redirect('instituicao:lista_tipos')
        else:
            tipos = TipoInstituicao.objects.all()
            messages.error(request, "Erro ao adicionar. Verifique os dados no formulário.")
            context = {'tipos': tipos, 'form': form}
            return render(request, self.template_name, context)

class TipoInstituicaoUpdateView(SuperuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TipoInstituicao
    form_class = TipoInstituicaoForm
    template_name = 'partials/generic_form.html'
    success_url = reverse_lazy('instituicao:lista_tipos')
    success_message = "Tipo de instituição atualizado com sucesso!"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Editar Tipo de Instituição'
        return context

class TipoInstituicaoDeleteView(SuperuserRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TipoInstituicao
    template_name = 'partials/generic_confirm_delete.html'
    success_url = reverse_lazy('instituicao:lista_tipos')
    success_message = "Tipo de instituição excluído com sucesso!"