import json
import crypto
import base64
import sys, os

# Diretórios base
dados_dir = "dados"

# --- Leitura ---

with open(f"{dados_dir}/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

with open(f"{dados_dir}/chave.json", "r", encoding="utf-8") as c:
    chave = json.load(c)

# --- Gravação ---
def gravar():
    with open(f"{dados_dir}/config.json", "w", encoding="utf-8") as fw:
        json.dump(config, fw, indent=4, ensure_ascii=False)

def gerar_chave():
    chave_leitura = open_key()
    #print(crypto.chave, " Valor da chave")

    if chave_leitura == "":
        gravar_chave(crypto.chave)


def open_key():
    chave_crypto = base64.b64decode(chave["crypto"]["key"])
    #print(chave_crypto, "valor recuperado")

    return chave_crypto

def gravar_chave(chave_gravar):

    #print(chave_gravar, " Valor da chave")
    chave_b64 = base64.b64encode(chave_gravar).decode("utf-8")
    chave["crypto"]["key"] = chave_b64
    with open(f"{dados_dir}/chave.json", "w", encoding="utf-8") as cw:
        json.dump(chave, cw, indent=4, ensure_ascii=False)

# Acessando dados
cliente = config["database"]["cliente"]
email = config["database"]["email"]
senha = crypto.recuperar_senha(open_key(),config["database"]["senhaemail"])
#print(senha)
caminho = config["database"]["caminhopasta"]
emails = config["database"]["emailsparaenvio"]
relatorio_str = config["database"]["relatorio"]
relatorio = relatorio_str.strip().lower() == "true"

dia = config["agendamento"]["dia"]
executado_str = config["agendamento"]["executado"]  # exemplo: "False"
executado = executado_str.strip().lower() == "true"

def atualizar_dados(dados):
    with open(f"{dados_dir}/config.json", "r", encoding="utf-8") as d:
        config = json.load(d)

    # Acessando dados
    cliente = config["database"]["cliente"]
    email = config["database"]["email"]
    senha = crypto.recuperar_senha(open_key(), config["database"]["senhaemail"])
    # print(senha)
    caminho = config["database"]["caminhopasta"]
    emails = config["database"]["emailsparaenvio"]

    dia = config["agendamento"]["dia"]
    executado_str = config["agendamento"]["executado"]  # exemplo: "False"
    executado = executado_str.strip().lower() == "true"

    if dados == "cliente":
        return cliente
    elif dados == "caminho":
        return caminho

## for email_envio in emails:
##     print("Enviando de:", email, "Enviando para:", email_envio)
### Exemplo de manipulação de dados ###
# -- print("Cliente:", config["database"]["cliente"])
# -- print("Email principal:", config["database"]["email"])
# -- print("Emails para envio:", config["database"]["emailsparaenvio"])

# --- Alteração ---
# -- config["database"]["cliente"] = "novo_cliente"
# -- config["database"]["emailsparaenvio"].append("novoemail@dominio.com")


