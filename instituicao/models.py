import os
from django.db import models
from django.utils.text import slugify

# --- Função de Upload Ajustada ---
def get_upload_path(instance, filename):
    """
    Gera um nome de arquivo padronizado para os brasões, baseado
    na instituição, cidade e UF. Formato:
    - brasoes/brasao_instituicao_guaira_sp.png
    - brasoes/brasao_municipio_guaira_sp.png
    """
    # Determina se é o brasão da instituição ou do município pelo nome do campo no modelo
    # Esta é uma forma robusta de saber qual campo está sendo salvo.
    if hasattr(instance, 'brasao_instituicao') and instance.brasao_instituicao.name == filename:
        tipo_brasao = 'instituicao'
    else:
        tipo_brasao = 'municipio'

    # Prepara os nomes para serem usados no caminho do arquivo (lowercase e sem espaços)
    cidade_slug = slugify(instance.municipio.nome)
    uf_slug = slugify(instance.municipio.estado.uf)
    ext = filename.split('.')[-1]

    # Monta o novo nome do arquivo no formato desejado
    novo_nome = f"brasao_{tipo_brasao}_{cidade_slug}_{uf_slug}.{ext}"
    
    # Retorna o caminho completo onde o arquivo será salvo
    return os.path.join('brasoes', novo_nome)


class Estado(models.Model):
    # ... (código do modelo Estado, sem alterações)
    nome = models.CharField(max_length=50, unique=True)
    uf = models.CharField(max_length=2, unique=True, verbose_name="UF")
    
    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Municipio(models.Model):
    # ... (código do modelo Municipio, sem alterações)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name="municipios")
    nome = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Município"
        verbose_name_plural = "Municípios"
        ordering = ['nome']
        unique_together = [['estado', 'nome']]

    def __str__(self):
        return f"{self.nome} - {self.estado.uf}"

class TipoInstituicao(models.Model):
    # ... (código do modelo TipoInstituicao, sem alterações)
    nome = models.CharField(max_length=150, unique=True, verbose_name="Nome do Tipo de Instituição")

    class Meta:
        verbose_name = "Tipo de Instituição"
        verbose_name_plural = "Tipos de Instituições"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Instituicao(models.Model):
    # ... (código do modelo Instituicao, apenas os campos de imagem são revisados aqui)
    tipo = models.ForeignKey(TipoInstituicao, on_delete=models.PROTECT, verbose_name="Tipo de Instituição", null=True, blank=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT, verbose_name="Município")
    
    nome_gerado = models.CharField(max_length=255, editable=False, verbose_name="Nome Gerado", null=True)
    
    cnpj = models.CharField(max_length=18, verbose_name="CNPJ", unique=True, blank=True, null=True, help_text="Formato: 00.000.000/0001-00")
    contato = models.CharField(max_length=100, verbose_name="Contato", blank=True, null=True, help_text="Nome do responsável ou telefone")
    email_institucional = models.EmailField(verbose_name="E-mail Institucional", blank=True, null=True)
    plano_contratado = models.CharField(max_length=50, verbose_name="Plano Contratado", blank=True, null=True)
    
    # Os campos de imagem agora usam a função de upload ajustada
    brasao_instituicao = models.ImageField(upload_to=get_upload_path, verbose_name="Brasão da Instituição", blank=True, null=True)
    brasao_municipio = models.ImageField(upload_to=get_upload_path, verbose_name="Brasão do Município", blank=True, null=True)
    
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")

    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"
        ordering = ['nome_gerado']
        unique_together = [['tipo', 'municipio']]

    def __str__(self):
        # Garante que o __str__ funcione mesmo se o nome ainda não foi gerado
        return self.nome_gerado if self.nome_gerado else f"Instituição ID {self.pk}"

    def save(self, *args, **kwargs):
        if self.tipo and self.municipio:
            self.nome_gerado = f"{self.tipo.nome} - {self.municipio.nome}-{self.municipio.estado.uf}"
        super().save(*args, **kwargs)