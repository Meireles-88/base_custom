from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .models import Instituicao

class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin para garantir que o usuário logado seja um superusuário (Admin Nível SI).
    """
    def test_func(self):
        return self.request.user.is_superuser

class InstituicaoAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Garante que o usuário seja um Superuser ou um Admin da instituição específica
    que está sendo acessada via URL.
    """
    def test_func(self):
        # O superusuário sempre tem acesso.
        if self.request.user.is_superuser:
            return True
        
        # Pega a instituição que está sendo acessada pela URL.
        # Espera que a URL tenha um parâmetro chamado 'pk' ou 'instituicao_pk'.
        instituicao_pk = self.kwargs.get('pk') or self.kwargs.get('instituicao_pk')
        if not instituicao_pk:
            return False # Se não houver ID da instituição na URL, nega o acesso.
            
        instituicao = get_object_or_404(Instituicao, pk=instituicao_pk)
        
        # Verifica se o usuário tem um perfil, pertence à instituição correta e é admin dela.
        return hasattr(self.request.user, 'userprofile') and \
               self.request.user.userprofile.instituicao == instituicao and \
               self.request.user.userprofile.is_admin_instituicao