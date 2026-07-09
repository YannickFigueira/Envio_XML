import base64
import os
from tinydb import TinyDB, Query

import crypto

desmontar_chave = 10 # Mudar para o número desejado

dados_dir = "dados"
if not os.path.exists(dados_dir):
    os.makedirs(dados_dir)

db = TinyDB('dados/xml_config.json')
tabela_config = db.table('configuracoes')
Config = Query()

# 1. Estrutura inicial padrão (Criada apenas na primeira vez que o script roda)
dados_backup = {
    "id_config": "global",
    "database": {
        "cliente": "cliente",
        "email": "exemplo@dominio.com.br",
        "senha_email": "",
        "caminho_sistema": "",
        "emails_para_envio": "exemplo1@dominio.com\nexemplo2@dominio.com\nexemplo3@dominio.com.br",
        "dia": 7,
        "executado": False,
        "sistema_emissor": "",
        "ultima_nota_danfe": "",
        "ultima_nota_nfce": "",
        "relatorio": True,
        "segundo_sistema": False,
        "segundo_sis_pasta": "",
        "modo_envio": "Telegram",
        "telegrambot": "",
        "chat_id": "",
        "crypto_key": ""
    }
}

# Inicializa o banco se estiver vazio
if not tabela_config.all():
    tabela_config.insert(dados_backup)

# --- FUNÇÃO PRINCIPAL DE MANIPULAÇÃO ---
# --- GRAVAR OS DADOS ---
def gravar_nova_tarefa(nome_tarefa):
    # 1. Busca o estado mais recente do banco
    config_atual = tabela_config.search(Config.id_config == "global")[0]

    # 2. Verifica se a tarefa já existe para não sobrescrever dados
    if nome_tarefa in config_atual['database']:
        print(f"Aviso: A tarefa '{nome_tarefa}' já existe!")
        return False

    # 3. Define a estrutura com os valores padrão para a nova tarefa
    config_atual['database'] = {
        "cliente": "Marmita",
        "email": "exemplo@dominio.com.br",
        "senha_email": "",
        "caminho_sistema": "C:\\Program Files (x86)\\Comercial",
        "emails_para_envio": [
            "exemplo1@dominio.com",
            "exemplo2@dominio.com",
            "exemplo3@dominio.com.br"
        ],
        "dia": "7",
        "executado": "True",
        "sistema_emissor": "Comercial",
        "ultima_nota_danfe": "000000017",
        "ultima_nota_nfce": "158506",
        "relatorio": "True",
        "segundo_sistema": "True",
        "segundo_sis_pasta": "",
        "modo_envio": "Telegram",
        "telegrambot": "",
        "chat_id": "",
        "crypto_key": ""
    }

    # 4. Salva de volta no TinyDB
    tabela_config.update(config_atual, Config.id_config == "global")
    print(f"Tarefa '{nome_tarefa}' adicionada com sucesso!")
    return True

def atualizar_dados(campo, valor):
    # 1. Busca o estado mais recente do banco de dados
    config_atual = tabela_config.search(Config.id_config == "global")[0]


    # 3. Altera cirurgicamente apenas o campo desejado na memória
    config_atual['database'][campo] = valor

    # 4. Grava de volta o documento inteiro atualizado
    tabela_config.update(config_atual, Config.id_config == "global")

# --- LEITURA DOS DADOS ---
def carregar_dados():
    config_atual = tabela_config.search(Config.id_config == "global")[0]

    return config_atual

# --- Utilização da chave ---
def embaralhar(texto, qtd):
    # Move as últimas 'qtd' letras para a frente
    return texto[-qtd:] + texto[:-qtd]

def restaurar(texto, qtd):
    # Move as primeiras 'qtd' letras para trás
    return texto[qtd:] + texto[:qtd]

def open_key(config_atual):
    chave_crypto = config_atual['database']['crypto_key']
    if not chave_crypto == "":
        chave_recuperada = chave_crypto
        chave_crypto = restaurar(chave_recuperada, desmontar_chave)

    return chave_crypto

def gerar_chave(config_atual):
    chave_leitura = open_key(config_atual)

    if chave_leitura == "":
        chave_desmontada = embaralhar(crypto.gerar_chave().decode('utf-8'), desmontar_chave)
        atualizar_dados('crypto_key', chave_desmontada)

def ler_dados_telegram(config_atual):
    if not config_atual["database"]["telegrambot"] == "":
        telegrambot = crypto.recuperar_cripto(open_key(config_atual), config_atual["database"]["telegrambot"])
        chat_id = crypto.recuperar_cripto(open_key(config_atual),  config_atual["database"]["chat_id"])
    else:
        telegrambot = ""
        chat_id = ""

    return telegrambot, chat_id