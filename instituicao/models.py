import os
from django.db import models
from django.utils.text import slugify

class Estado(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    uf = models.CharField(max_length=2, unique=True, verbose_name="UF")
    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ['nome']
    def __str__(self): return self.nome

class Municipio(models.Model):
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name="municipios")
    nome = models.CharField(max_length=150)
    class Meta:
        verbose_name = "Município"
        verbose_name_plural = "Municípios"
        ordering = ['nome']
        unique_together = [['estado', 'nome']]
    def __str__(self): return f"{self.nome} - {self.estado.uf}"

class TipoInstituicao(models.Model):
    nome = models.CharField(max_length=150, unique=True, verbose_name="Nome do Tipo de Instituição")
    class Meta:
        verbose_name = "Tipo de Instituição"
        verbose_name_plural = "Tipos de Instituições"
        ordering = ['nome']
    def __str__(self): return self.nome

def get_upload_path(instance, filename):
    tipo_brasao = 'instituicao' if hasattr(instance, 'brasao_instituicao') and instance.brasao_instituicao.name == filename else 'municipio'
    cidade_slug = slugify(instance.municipio.nome)
    uf_slug = slugify(instance.municipio.estado.uf)
    ext = filename.split('.')[-1]
    novo_nome = f"brasao_{tipo_brasao}_{cidade_slug}_{uf_slug}.{ext}"
    return os.path.join('brasoes', novo_nome)

class Instituicao(models.Model):
    tipo = models.ForeignKey(TipoInstituicao, on_delete=models.PROTECT, verbose_name="Tipo de Instituição")
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT, verbose_name="Município")
    nome_gerado = models.CharField(max_length=255, editable=False, verbose_name="Nome Gerado")
    logradouro = models.CharField(max_length=255, verbose_name="Logradouro", blank=True, null=True, help_text="Ex: Rua, Avenida, Praça...")
    numero = models.CharField(max_length=20, verbose_name="Número", blank=True, null=True)
    bairro = models.CharField(max_length=100, verbose_name="Bairro", blank=True, null=True)
    cep = models.CharField(max_length=9, verbose_name="CEP", blank=True, null=True, help_text="Formato: 00000-000")
    cnpj = models.CharField(max_length=18, verbose_name="CNPJ", blank=True, null=True, help_text="Formato: 00.000.000/0001-00")
    contato = models.CharField(max_length=100, verbose_name="Contato", blank=True, null=True)
    email_institucional = models.EmailField(verbose_name="E-mail Institucional", blank=True, null=True)
    plano_contratado = models.CharField(max_length=50, verbose_name="Plano Contratado", blank=True, null=True)
    brasao_instituicao = models.ImageField(upload_to=get_upload_path, verbose_name="Brasão da Instituição", blank=True, null=True)
    brasao_municipio = models.ImageField(upload_to=get_upload_path, verbose_name="Brasão do Município", blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"
        ordering = ['nome_gerado']
        unique_together = [['tipo', 'municipio']]

    def __str__(self):
        return self.nome_gerado if self.nome_gerado else f"ID: {self.pk}"

    def save(self, *args, **kwargs):
        if self.tipo and self.municipio:
            self.nome_gerado = f"{self.tipo.nome} - {self.municipio.nome}-{self.municipio.estado.uf}"
        super().save(*args, **kwargs)