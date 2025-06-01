import json
import os

# Altere o nome do arquivo para .json
CAMINHO_ARQUIVO = 'dicionario.json'

def carregar_termos():
    """
    Carrega os termos do dicionário de um arquivo JSON.
    Retorna um dicionário com os termos e suas definições.
    Cria um arquivo vazio se ele não existir ou estiver corrompido.
    """
    termos = {}
    if os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, 'r', encoding='utf-8') as f:
            try:
                # Tenta carregar o JSON
                termos = json.load(f)
            except json.JSONDecodeError:
                # Se o arquivo estiver corrompido ou vazio, inicializa como vazio
                print(f"Aviso: Arquivo '{CAMINHO_ARQUIVO}' está vazio ou corrompido. Inicializando dicionário vazio.")
                termos = {}
            except Exception as e:
                # Captura outros erros de leitura
                print(f"Erro ao carregar dicionário de '{CAMINHO_ARQUIVO}': {e}. Inicializando dicionário vazio.")
                termos = {}
    return termos

def salvar_termos(termos):
    """
    Salva os termos do dicionário em um arquivo JSON.
    """
    with open(CAMINHO_ARQUIVO, 'w', encoding='utf-8') as f:
        # Usa json.dump para escrever o dicionário no arquivo
        # indent=4 torna o JSON legível com indentação
        # ensure_ascii=False permite caracteres UTF-8 diretamente
        json.dump(termos, f, indent=4, ensure_ascii=False)