# gerar_estrutura.py
import os

# --- CONFIGURAÇÕES ---

# 1. Pasta raiz do projeto (o '.' significa a pasta atual onde o script está)
ROOT_DIRECTORY = '.'

# 2. Pastas e arquivos que você quer ignorar completamente
#    Adicione outros nomes se precisar, como '.vscode', 'node_modules', etc.
IGNORE_LIST = {
    'venv',
    '__pycache__',
    '.git',
    '.idea',
    'db.sqlite3',
    'gerar_estrutura.py', # Para não listar o próprio script
    'estrutura_do_projeto.txt' # E nem o arquivo de saída
}

# 3. Nome do arquivo que será gerado com a árvore
OUTPUT_FILENAME = 'estrutura_do_projeto.txt'

# --- FIM DAS CONFIGURAÇÕES ---


def generate_tree(directory, prefix=""):
    """Função recursiva para gerar a árvore de diretórios e arquivos."""
    try:
        # Pega todos os itens no diretório e os ordena
        # os.scandir é mais eficiente que os.listdir
        entries = sorted(os.scandir(directory), key=lambda e: e.name)
    except FileNotFoundError:
        return

    # Filtra os itens da IGNORE_LIST
    entries = [e for e in entries if e.name not in IGNORE_LIST]
    
    for i, entry in enumerate(entries):
        # Determina o conector da árvore: '├──' para itens no meio, '└──' para o último
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        
        # Escreve a linha no arquivo
        file_handle.write(f"{prefix}{connector}{entry.name}\n")
        
        # Se o item for um diretório, chama a função para ele (recursão)
        if entry.is_dir():
            new_prefix = prefix + ("    " if is_last else "│   ")
            generate_tree(entry.path, prefix=new_prefix)

# --- EXECUÇÃO PRINCIPAL ---

print(f"Gerando a árvore do projeto. Ignorando: {IGNORE_LIST}")

# Abre o arquivo de saída para escrita com codificação UTF-8
with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as file_handle:
    # Escreve o nome da pasta raiz no topo do arquivo
    # Pega o nome da pasta atual de forma limpa
    root_name = os.path.basename(os.path.abspath(ROOT_DIRECTORY))
    file_handle.write(f"{root_name}/\n")
    
    # Inicia a geração da árvore
    generate_tree(ROOT_DIRECTORY)

print(f"\nFeito! A estrutura do projeto foi salva em '{OUTPUT_FILENAME}'.")

