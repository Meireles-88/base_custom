# usuario/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    cidade_uf = models.CharField(
        max_length=100,
        verbose_name=_("Cidade - UF"),
        help_text=_("Exemplo: Guaira - SP"),
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name=_("E-mail"),
        blank=True,
        null=True
    )
    cpf = models.CharField(
        max_length=14,  # Considerando formato com máscara (ex.: 123.456.789-00)
        verbose_name=_("CPF"),
        blank=True,
        null=True
    )
    celular = models.CharField(
        max_length=15,  # Considerando formato com máscara (ex.: (11) 98765-4321)
        verbose_name=_("Celular"),
        blank=True,
        null=True
    )
    fone = models.CharField(
        max_length=14,  # Considerando formato com máscara (ex.: (11) 1234-5678)
        verbose_name=_("Telefone"),
        blank=True,
        null=True
    )
    foto = models.ImageField(
        upload_to='profile_photos/',
        verbose_name=_("Foto do Usuário"),
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
        permissions = [
            ('can_add_userprofile', 'Can add user profile'),
            ('can_change_userprofile', 'Can change user profile'),
            ('can_delete_userprofile', 'Can delete user profile'),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.cargo or 'Sem cargo'}"

# --- INÍCIO DA MODIFICAÇÃO ---

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, **kwargs):
    """
    Este sinal garante que um UserProfile seja criado para cada User, caso não exista.
    Ele usa get_or_create para evitar o erro 'RelatedObjectDoesNotExist'.
    """
    # A linha abaixo tenta obter o perfil do usuário. Se não existir, ela o cria.
    # Isso resolve o problema para usuários novos e para usuários antigos (como o admin)
    # que foram criados antes do sistema de perfis.
    UserProfile.objects.get_or_create(user=instance)

# --- FIM DA MODIFICAÇÃO ---