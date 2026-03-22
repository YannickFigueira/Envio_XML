import json

# --- Leitura ---
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Acessando dados
cliente = config["database"]["cliente"]
email = config["database"]["email"]
senha = config["database"]["senhaemail"]
caminho = config["database"]["caminhopasta"]
emails = config["database"]["emailsparaenvio"]
## print(cliente)
## print(email)
## print(senha)
## print(caminho)

## for email_envio in emails:
##     print("Enviando de:", email, "Enviando para:", email_envio)
### Exemplo de manipulação de dados ###
# -- print("Cliente:", config["database"]["cliente"])
# -- print("Email principal:", config["database"]["email"])
# -- print("Emails para envio:", config["database"]["emailsparaenvio"])

# --- Alteração ---
# -- config["database"]["cliente"] = "novo_cliente"
# -- config["database"]["emailsparaenvio"].append("novoemail@dominio.com")

# --- Gravação ---
def gravar():
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
