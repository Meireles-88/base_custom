# instituicao/mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .models import Instituicao

class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """ Garante que o usuário logado seja um superusuário (Admin Nível SI). """
    def test_func(self):
        return self.request.user.is_superuser

class InstituicaoAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """ Garante que o usuário seja um Superuser OU um Admin da instituição específica. """
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        instituicao_pk = self.kwargs.get('pk') or self.kwargs.get('instituicao_pk')
        if not instituicao_pk:
            return False
        instituicao = get_object_or_404(Instituicao, pk=instituicao_pk)
        return hasattr(self.request.user, 'userprofile') and \
               self.request.user.userprofile.instituicao == instituicao and \
               self.request.user.userprofile.is_admin_instituicao