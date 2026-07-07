import os
from tinydb import TinyDB, Query

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
        "cliente": "Marmita",
        "email": "exemplo@dominio.com.br",
        "senhaemail": "",
        "caminhopasta": "C:\\Program Files (x86)\\Comercial",
        "emailsparaenvio": [
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
        "modoenvio": "Telegram",
        "telegrambot": "",
        "chat_id": ""
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
        "senhaemail": "",
        "caminhopasta": "C:\\Program Files (x86)\\Comercial",
        "emailsparaenvio": [
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
        "modoenvio": "Telegram",
        "telegrambot": "",
        "chat_id": ""
    }

    # 4. Salva de volta no TinyDB
    tabela_config.update(config_atual, Config.id_config == "global")
    print(f"Tarefa '{nome_tarefa}' adicionada com sucesso!")
    return True

def atualizar_campo_database(campo, valor):
    # 1. Busca o estado mais recente do banco de dados
    config_atual = tabela_config.search(Config.id_config == "global")[0]


    # 3. Altera cirurgicamente apenas o campo desejado na memória
    config_atual['database'][campo] = valor

    # 4. Grava de volta o documento inteiro atualizado
    tabela_config.update(config_atual, Config.id_config == "global")

# --- LEITURA DOS DADOS ---
def carregar_dados_database():
    config_atual = tabela_config.search(Config.id_config == "global")[0]

    return config_atual