# usuario/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    """
    Modelo para estender o usuário padrão do Django com informações adicionais,
    como cargo e associação a uma instituição.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Usuário"))
    cargo = models.CharField(
        max_length=100,
        verbose_name=_("Cargo"),
        help_text=_("Exemplo: Guarda, Supervisor, Administrador"),
        blank=True,
        null=True
    )
    instituicao = models.CharField(
        max_length=200,
        verbose_name=_("Instituição"),
        help_text=_("Nome da instituição associada, ex.: Guarda Civil Municipal"),
        blank=True,
        null=True
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Data de Criação")
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name=_("Ativo")
    )

    class Meta:
        verbose_name = _("Perfil de Usuário")
        verbose_name_plural = _("Perfis de Usuários")
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.username} - {self.cargo or 'Sem cargo'}"

    def save(self, *args, **kwargs):
        # Garante que o perfil seja criado automaticamente ao criar um usuário
        if not self.pk and not UserProfile.objects.filter(user=self.user).exists():
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)