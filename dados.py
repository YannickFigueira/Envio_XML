import json
import crypto
import base64

# Diretórios base
dados_dir = "dados"

# --- Leitura ---
with open(f"{dados_dir}/chave.json", "r", encoding="utf-8") as c:
    chave = json.load(c)

def open_key():
    chave_crypto = base64.b64decode(chave["crypto"]["key"])
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
    chave["crypto"]["key"] = chave_b64
    with open(f"{dados_dir}/chave.json", "w", encoding="utf-8") as cw:
        json.dump(chave, cw, indent=4, ensure_ascii=False)

def gerar_chave():
    chave_leitura = open_key()
    # print(crypto.chave, " Valor da chave")

    if chave_leitura == "":
        gravar_chave(crypto.chave)

def ler_dados(dados):
    with open(f"{dados_dir}/config.json", "r", encoding="utf-8") as d:
        config = json.load(d)

    # Acessando dados
    cliente = config["database"]["cliente"]
    email = config["database"]["email"]
    senha = crypto.recuperar_senha(open_key(), config["database"]["senhaemail"])
    caminho = config["database"]["caminhopasta"]
    emails = config["database"]["emailsparaenvio"]
    relatorio_str = config["database"]["relatorio"]
    relatorio = relatorio_str.strip().lower() == "true"
    modoenvio = config["database"]["chat_id"]
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
    elif dados == "modoenvio":
        return modoenvio
    elif dados == "telegrambot":
        return telegrambot
    elif dados == "chat_id":
        return chat_id
    elif dados == "dia":
        return dia
    elif dados == "executado":
        return executado
    return None


