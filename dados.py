import json
import os

import crypto
import base64

adicionar_dados = ""

# Dados iniciais
dados_chave = {
    "app": {
        "name": "EnvioXML",
        "version": "4.0.0"
    },
    "crypto": {
        "key": ""
    }
}

dados_config = {
    "app": {
        "name": "EnvioXML",
        "version": "4.0.0"
    },
    "database": {
        "cliente": "cliente",
        "email": "exemplo@dominio.com.br",
        "senhaemail": "",
        "caminhopasta": "",
        "emailsparaenvio": [
            "exemplo1@dominio.com",
            "exemplo2@dominio.com",
            "exemplo3@dominio.com.br"
        ],
        "dia": "7",
        "executado": "False",
        "sistema_emissor": "",
        "ultima_nota_danfe": "",
        "ultima_nota_nfce": "",
        "relatorio": "True",
        "modoenvio": "Telegram",
        "telegrambot": "",
        "chat_id": ""
    }}

# Diretórios base
dados_dir = "dados"

if not os.path.exists(dados_dir):
    os.makedirs(dados_dir)

    with open(f"{dados_dir}/chave.json", "w", encoding="utf-8") as c:
        json.dump(dados_chave, c, indent=4, ensure_ascii=False)

    with open(f"{dados_dir}/config.json", "w", encoding="utf-8") as c:
        json.dump(dados_config, c, indent=4, ensure_ascii=False)

# --- Leitura ---
with open(f"{dados_dir}/chave.json", "r", encoding="utf-8") as c:
    chave = json.load(c)

def open_key():
    valor_chave = chave["crypto"]["key"]
    if not valor_chave == "":
        separar_chave = chave["crypto"]["key"].split("__")
        chave_crypto = base64.b64decode(separar_chave[0])
    else:
        chave_crypto = chave["crypto"]["key"]
    # print(chave_crypto, "valor recuperado")

    return chave_crypto

# --- Gravação ---
def gravar_dados(campo, valor):
    with open(f"{dados_dir}/config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    if campo == "emailsparaenvio":
        emails_separate = valor.split("\n")
        config["database"]["emailsparaenvio"].clear()
        for separate in emails_separate:
            if separate != "":
                config["database"]["emailsparaenvio"].append(separate)
    else:
        config["database"][campo] = valor

    with open(f"{dados_dir}/config.json", "w", encoding="utf-8") as fw:
        json.dump(config, fw, indent=4, ensure_ascii=False)

def gravar_chave(chave_gravar):
    # print(chave_gravar, " Valor da chave")
    chave_b64 = base64.b64encode(chave_gravar).decode("utf-8")
    chave["crypto"]["key"] = f"{chave_b64}__{adicionar_dados}"
    with open(f"{dados_dir}/chave.json", "w", encoding="utf-8") as cw:
        json.dump(chave, cw, indent=4, ensure_ascii=False)

def gerar_chave():
    chave_leitura = open_key()
    # print(crypto.chave, " Valor da chave")

    if chave_leitura == "":
        gravar_chave(crypto.pegar_chave())

def ler_dados(dados):
    with open(f"{dados_dir}/config.json", "r", encoding="utf-8") as d:
        config = json.load(d)

    # Acessando dados
    cliente = config["database"]["cliente"]
    email = config["database"]["email"]
    if not config["database"]["senhaemail"] == "":
        senha = crypto.recuperar_senha(open_key(), config["database"]["senhaemail"])
    else:
        senha = ""
    caminho = config["database"]["caminhopasta"]
    emails = config["database"]["emailsparaenvio"]
    relatorio_str = config["database"]["relatorio"]
    relatorio = relatorio_str.strip().lower() == "true"
    sistema_emissor = config["database"]["sistema_emissor"]
    modoenvio = config["database"]["modoenvio"]
    telegrambot = config["database"]["telegrambot"]
    chat_id = config["database"]["chat_id"]

    dia = config["database"]["dia"]
    executado_str = config["database"]["executado"]  # exemplo: "False"
    executado = executado_str.strip().lower() == "true"

    if dados == "cliente":
        return cliente
    elif dados == "email":
        return email
    elif dados == "senha":
        return senha
    elif dados == "caminho":
        return caminho
    elif dados == "emailsparaenvio":
        return emails
    elif dados == "relatorio":
        return relatorio
    elif dados == "sistema_emissor":
        return sistema_emissor
    elif dados == "modoenvio":
        return modoenvio
    elif dados == "telegrambot":
        return telegrambot
    elif dados == "chat_id":
        return chat_id
    elif dados == "dia":
        return int(dia)
    elif dados == "executado":
        return executado
    return None


