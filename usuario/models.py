# usuario/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from instituicao.models import Instituicao

class Cargo(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Cargo")
    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ['nome']
    def __str__(self): return self.nome

class Patente(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Patente")
    ordem = models.PositiveIntegerField(default=0, help_text="Usado para ordenar por hierarquia (menor para maior)")
    class Meta:
        verbose_name = "Patente"
        verbose_name_plural = "Patentes"
        ordering = ['ordem']
    def __str__(self): return self.nome

class UserProfile(models.Model):
    class StatusVinculo(models.TextChoices):
        SEM_VINCULO = 'SV', _('Sem Vínculo')
        PENDENTE = 'PE', _('Pendente')
        ATIVO = 'AT', _('Ativo')
        REJEITADO = 'RJ', _('Rejeitado')

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Usuário"))
    instituicao = models.ForeignKey(Instituicao, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Instituição Vinculada"))
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Cargo"))
    patente = models.ForeignKey(Patente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Patente"))
    status_vinculo = models.CharField(max_length=2, choices=StatusVinculo.choices, default=StatusVinculo.SEM_VINCULO, verbose_name="Status do Vínculo")
    is_admin_instituicao = models.BooleanField(default=False, verbose_name="É Administrador da Instituição")
    cpf = models.CharField(max_length=14, verbose_name=_("CPF"), blank=True, null=True)
    celular = models.CharField(max_length=15, verbose_name=_("Celular"), blank=True, null=True)
    foto = models.ImageField(upload_to='profile_photos/', verbose_name=_("Foto do Perfil"), blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name=_("Data de Criação do Perfil"))

    class Meta:
        verbose_name = _("Perfil de Usuário")
        verbose_name_plural = _("Perfis de Usuários")
        ordering = ['user__username']

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)