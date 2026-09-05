import webbrowser

import requests
import caixa_mensagem

# Substitua pelo seu repositório
def consultar_lancamento(repo, version):
    owner = "YannickFigueira"
    #repo = "CopiarArquivos"

    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    pagina = f"https://github.com/{owner}/{repo}/releases"

    response = requests.get(url)
    if response.status_code == 200:
        release = response.json()
        if not release["tag_name"] == version:
            #messagebox.showinfo("Lancamento", f"Nova versão\n{release['name']}")

            resposta = caixa_mensagem.sim_nao(
                "Lançamento",
                f"Nova versão: {release['name']}\n\nDeseja abrir o link de download?"
            )

            if resposta == "Sim":
                webbrowser.open(pagina)
            #print("Última versão:", release["tag_name"])
            #print("Nome:", release["name"])
            #print("Publicado em:", release["published_at"])
        else:
            caixa_mensagem.info("Lancamento", "Já está usando a versão mais recente")
    else:
        caixa_mensagem.cuidado("Erro ao consultar:", "Repositório não encontrado")
