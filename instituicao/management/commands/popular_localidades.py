# instituicao/management/commands/popular_localidades.py

import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from instituicao.models import Estado, Municipio

class Command(BaseCommand):
    help = 'Popula o banco de dados com Estados e Municípios do Brasil usando a API do IBGE.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando a população de Estados e Municípios...'))

        try:
            with transaction.atomic():
                # URL da API do IBGE para estados
                estados_url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome'
                
                self.stdout.write('Buscando estados na API do IBGE...')
                response_estados = requests.get(estados_url)
                response_estados.raise_for_status()  # Lança um erro se a requisição falhar
                estados_data = response_estados.json()

                for estado_data in estados_data:
                    # Usamos get_or_create para evitar duplicatas
                    estado, created = Estado.objects.get_or_create(
                        uf=estado_data['sigla'],
                        defaults={'nome': estado_data['nome']}
                    )
                    
                    if created:
                        self.stdout.write(f'Estado "{estado.nome}" criado.')

                    # URL da API para municípios do estado atual
                    municipios_url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado.uf}/municipios"
                    
                    self.stdout.write(f'Buscando municípios de {estado.nome}...')
                    response_municipios = requests.get(municipios_url)
                    response_municipios.raise_for_status()
                    municipios_data = response_municipios.json()

                    for municipio_data in municipios_data:
                        # Usamos get_or_create para cada município
                        municipio, created_mun = Municipio.objects.get_or_create(
                            estado=estado,
                            nome=municipio_data['nome']
                        )
                        if created_mun:
                            self.stdout.write(f'  - Município "{municipio.nome}" criado.')

            self.stdout.write(self.style.SUCCESS('População de dados concluída com sucesso!'))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Erro ao se conectar com a API do IBGE: {e}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ocorreu um erro inesperado: {e}'))