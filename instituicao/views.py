from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect

# Importações de Modelos, Formulários e Mixins
from .models import Instituicao, TipoInstituicao, Estado, Municipio
from usuario.models import UserProfile
from .forms import InstituicaoForm, TipoInstituicaoForm
from usuario.forms import CargoForm, PatenteForm, FuncaoForm
from .mixins import SuperuserRequiredMixin, InstituicaoAdminRequiredMixin



# --- VIEWS PARA MUDANÇA DE CONTEXTO ---
@login_required
def entrar_contexto_institucional(request, pk):
    """ Salva na sessão o ID da instituição que o Admin SI quer gerenciar e o redireciona. """
    if not request.user.is_superuser:
        messages.error(request, "Acesso não permitido.")
        return redirect('painel:dashboard')
    
    instituicao = get_object_or_404(Instituicao, pk=pk)
    request.session['managing_institution_id'] = instituicao.pk
    messages.info(request, f"Você agora está gerenciando a instituição: {instituicao.nome_gerado}")
    
    # Redireciona para o perfil da instituição, agora DENTRO do novo contexto
    return redirect('instituicao:detalhe_instituicao', pk=instituicao.pk)

@login_required
def sair_contexto_institucional(request):
    """ Limpa da sessão o ID da instituição, retornando o Admin SI à visão global (Lobby). """
    if 'managing_institution_id' in request.session:
        del request.session['managing_institution_id']
        messages.info(request, "Você retornou à Visão Global do Administrador SI.")
        
    return redirect('painel:dashboard')



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

# --- VIEW UNIFICADA PARA GERENCIAR HIERARQUIA ---
class GerenciarHierarquiaView(BaseGerenciarView, View):
    template_name = 'instituicao/gerenciar/gerenciar_hierarquia.html'

    def get_context_data(self, **kwargs):
        # A instituicao já é definida no dispatch da classe base
        context = super().get_context_data(**kwargs)
        context.update({
            'cargos': Cargo.objects.filter(instituicao=self.instituicao),
            'patentes': Patente.objects.filter(instituicao=self.instituicao),
            'funcoes': Funcao.objects.filter(instituicao=self.instituicao),
            'cargo_form': CargoForm(),
            'patente_form': PatenteForm(),
            'funcao_form': FuncaoForm(),
        })
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form_type = request.POST.get('form_type')
        form_map = {'cargo': CargoForm, 'patente': PatenteForm, 'funcao': FuncaoForm}
        
        form_class = form_map.get(form_type)
        if not form_class:
            messages.error(request, "Ação inválida.")
            return redirect('instituicao:gerenciar_instituicao', pk=self.instituicao.pk)

        form = form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.instituicao = self.instituicao
            instance.save()
            messages.success(request, f"{form.Meta.model._meta.verbose_name.title()} adicionado com sucesso!")
        else:
            context = self.get_context_data(**kwargs)
            context[f'{form_type}_form'] = form
            messages.error(request, f"Erro ao adicionar: {next(iter(form.errors.values()))[0]}")
            return render(request, self.template_name, context)
            
        return redirect('instituicao:gerenciar_hierarquia', instituicao_pk=self.instituicao.pk)


# --- Views de Tipo de Instituição (Global) ---
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