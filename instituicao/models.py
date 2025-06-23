import os
from django.db import models
from django.utils.text import slugify

# NOVO MODELO para padronizar os tipos de instituição
class TipoInstituicao(models.Model):
    """
    Modelo para armazenar os tipos padronizados de instituições.
    Ex: 'Guarda Civil Municipal', 'Polícia Militar', 'Corpo de Bombeiros'.
    Este modelo será gerenciado pelo admin do sistema (SI).
    """
    nome = models.CharField(max_length=150, unique=True, verbose_name="Nome do Tipo de Instituição")

    class Meta:
        verbose_name = "Tipo de Instituição"
        verbose_name_plural = "Tipos de Instituições"
        ordering = ['nome']

    def __str__(self):
        return self.nome

# --- Função de Upload Ajustada ---
def get_upload_path(instance, filename):
    """
    Função ajustada para usar o nome do tipo de instituição.
    """
    tipo_brasao = 'instituicao' if 'instituicao' in filename else 'municipio'
    
    # Usa o nome do tipo de instituição e o município para o slug
    tipo_slug = slugify(instance.tipo.nome)
    municipio_slug = slugify(instance.municipio)
    ext = filename.split('.')[-1]

    novo_nome = f"brasao_{tipo_brasao}_{tipo_slug}_{municipio_slug}-{instance.uf}.{ext}"
    return os.path.join('brasoes', novo_nome)

# --- Modelo Principal Ajustado ---
class Instituicao(models.Model):
    """
    Modelo para armazenar uma instituição específica em um município.
    """
    # O campo 'nome' foi substituído por uma relação com TipoInstituicao
    tipo = models.ForeignKey(
        TipoInstituicao, 
        on_delete=models.PROTECT, # Impede a exclusão de um tipo se estiver em uso
        verbose_name="Tipo de Instituição",
        null=True, 
        blank=True  
    )
    municipio = models.CharField(max_length=100, verbose_name="Município")
    uf = models.CharField(max_length=2, verbose_name="UF", help_text="Ex: SP, RJ")
    
    # CNPJ agora é o principal identificador único
    cnpj = models.CharField(
        max_length=18, 
        verbose_name="CNPJ", 
        unique=True, # Garante que o CNPJ seja único em todo o sistema
        blank=True, 
        null=True, 
        help_text="Formato: 00.000.000/0001-00"
    )
    
    contato = models.CharField(max_length=100, verbose_name="Contato", blank=True, null=True, help_text="Nome do responsável ou telefone")
    plano_contratado = models.CharField(max_length=50, verbose_name="Plano Contratado", blank=True, null=True)
    brasao_instituicao = models.ImageField(upload_to=get_upload_path, verbose_name="Brasão da Instituição", blank=True, null=True)
    brasao_municipio = models.ImageField(upload_to=get_upload_path, verbose_name="Brasão do Município", blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"
        ordering = ['tipo__nome', 'municipio']
        # Garante que não se pode cadastrar o mesmo tipo de instituição para a mesma cidade
        unique_together = [['tipo', 'municipio', 'uf']]

    def __str__(self):
        # A representação textual agora usa o nome do tipo
        return f"{self.tipo.nome} - {self.municipio}/{self.uf}"