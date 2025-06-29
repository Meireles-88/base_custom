from instituicao.models import Instituicao
from usuario.models import UserProfile
from django.urls import reverse, NoReverseMatch

def institutional_context(request):
    """
    Este processador de contexto define a 'instituicao_ativa' para
    ser usada em todo o sistema, especialmente nos templates base.
    """
    instituicao_ativa = None
    
    # Primeiro, verifica se um Admin SI está gerenciando uma instituição específica
    if request.user.is_superuser and 'managing_institution_id' in request.session:
        try:
            instituicao_ativa = Instituicao.objects.get(pk=request.session.get('managing_institution_id'))
        except Instituicao.DoesNotExist:
            del request.session['managing_institution_id']

    # Se não, verifica se o usuário logado pertence a uma instituição
    elif request.user.is_authenticated and hasattr(request.user, 'userprofile'):
        instituicao_ativa = request.user.userprofile.instituicao

    return {
        'instituicao_ativa': instituicao_ativa
    }


def set_breadcrumb(request):
    """
    Gera o breadcrumb de navegação de forma mais robusta e centralizada.
    """
    breadcrumb = []
    
    # Ponto de partida
    if request.user.is_authenticated:
        breadcrumb.append({'title': 'Meu Painel', 'url': reverse('painel:dashboard')})
    else:
        # Para páginas públicas, o breadcrumb pode ser definido na própria view, se necessário
        return {'breadcrumb': [{'title': 'Início', 'url': reverse('painel:home')}]}

    # Lógica para o segundo nível (ex: /instituicoes/)
    try:
        resolver_match = request.resolver_match
        if resolver_match:
            app_name = resolver_match.app_name
            
            if app_name == 'instituicao' and resolver_match.view_name != 'painel:dashboard':
                breadcrumb.append({'title': 'Instituições', 'url': reverse('instituicao:lista_instituicoes')})
            elif app_name == 'usuario' and resolver_match.view_name != 'painel:dashboard':
                 breadcrumb.append({'title': 'Usuários', 'url': reverse('usuario:user_list')})

            # Adicione outras lógicas para apps futuros aqui

    except NoReverseMatch:
        pass # Ignora erros se a URL não puder ser resolvida

    return {'breadcrumb': breadcrumb}