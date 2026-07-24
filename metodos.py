import os, shutil
import threading
import zipfile
from pathlib import Path
from platform import system
from tkinter import messagebox, filedialog
import logging
from datetime import datetime
### Módulos próprios
import dados

# Variáveis
home_dir = os.path.expanduser('~')
system = system()
if system == 'Linux':
    if not os.path.exists(f"{home_dir}/log"):
        os.mkdir(f"{home_dir}/log")

    logging.basicConfig(
        filename=f"{home_dir}/log/envio_xml.log",        # nome do arquivo
        level=logging.ERROR,         # nível de log
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
elif system == 'Windows':
    if not os.path.exists(f"c:/temp"):
        os.mkdir(f"c:/temp")

    logging.basicConfig(
        filename="c:/temp/compactar.log",  # nome do arquivo
        level=logging.ERROR,  # nível de log
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def copiar_xmls(origem, destino_dir, cliente, mes_desejado, ano_desejado, sistema_emissor):
    destino_compactar = ""
    if sistema_emissor == "SmallSoft":
        dir_nfce = f"\\nfce"
    else:
        dir_nfce = ""

    if system == "Windows":
        destino_compactar = f"{destino_dir}\\{ano_desejado}_{mes_desejado}_{cliente}"
        destino_dir = f"{destino_dir}\\{ano_desejado}_{mes_desejado}_{cliente}\\notas{dir_nfce}"
        if not os.path.exists(destino_dir):
            os.makedirs(destino_dir)
            if not os.path.exists(f"{destino_compactar}\\relatorio"): os.makedirs(f"{destino_compactar}\\relatorio")
    elif system == "Linux":
        destino_compactar = f"{destino_dir}/{ano_desejado}_{mes_desejado}_{cliente}"
        destino_dir = f"{destino_dir}/{ano_desejado}_{mes_desejado}_{cliente}/notas"
        if not os.path.exists(destino_dir):
            os.makedirs(destino_dir)
            if not os.path.exists(f"{destino_compactar}/relatorio"): os.makedirs(f"{destino_compactar}/relatorio")

    qtd_arquivos = False
    for arquivo in os.listdir(origem):
        caminho_arquivo = os.path.join(origem, arquivo)

        if os.path.isfile(caminho_arquivo):
            # Obter data de criação
            timestamp_modificacao = os.path.getmtime(caminho_arquivo)
            data_modificacao = datetime.fromtimestamp(timestamp_modificacao)

            # Verificar se o arquivo pertence ao mês/ano desejado
            if data_modificacao.month == mes_desejado and data_modificacao.year == ano_desejado:
                qtd_arquivos = True
                shutil.copy2(caminho_arquivo, destino_dir)

    if qtd_arquivos:
        return qtd_arquivos
    else:
        shutil.rmtree(destino_compactar)
        return False

resultado = {}
def compactar(origem, destino_zip, mes_desejado, ano_desejado, filial, out):
    mes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    if not origem == "":
        pasta_origem = Path(origem)
        if pasta_origem.is_dir() or pasta_origem.is_file():
            if not destino_zip == "":
                if system == 'Linux':
                    destino_zip = f"{destino_zip}/{ano_desejado}_{mes[mes_desejado - 1]}_{dados.ler_dados('cliente')}{filial}.zip"
                elif system == 'Windows':
                    destino_zip = f"{destino_zip}\\{ano_desejado}_{mes[mes_desejado - 1]}_{dados.ler_dados('cliente')}{filial}.zip"
                # Cria o arquivo ZIP no destino

                with zipfile.ZipFile(destino_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    # Percorre todos os arquivos da pasta de origem
                    contador = 0
                    # Conta todos os arquivos dentro da pasta origem
                    #total = sum(len(arquivos) for _, _, arquivos in os.walk(origem))

                    for raiz, _, arquivos in os.walk(origem):
                        for arquivo in arquivos:

                            try:
                                caminho_completo = Path(raiz) / arquivo
                                caminho_relativo = caminho_completo.relative_to(origem)
                                zipf.write(caminho_completo, caminho_relativo)

                                #atualizar_barra(contador, total, progress_canvas)
                                contador += 1
                            except Exception as e:
                                logging.error(f"Erro ao compactar {caminho_completo}: {e}")
                shutil.rmtree(origem)
                    #atualizar_barra(total, total, progress_canvas)
                    #messagebox.showinfo("Completo", "Finalizado com exito.")
            #else:
                #messagebox.showinfo("Verificar", "Digite algo ou selecione uma pasta.")
        #else:
            #messagebox.showinfo("Verificar", "Arquivo ou pasta inexistente")
    #else:
        #messagebox.showinfo("Verificar", "Digite algo ou selecione uma pasta")

    out["arquivo"] = destino_zip

def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione uma pasta")
    if pasta:  # se o usuário não cancelar
        return pasta
    else:
        return ""

def verificar_sistema(sistema_emissor):
    resposta = False
    caminho = ""
    if sistema_emissor == "SmallSoft":
        resposta = messagebox.askyesno("Escolha", f"Sistema selecionado {sistema_emissor}\nQuer usar a pasta padrão")
        caminho = "C:\\Program Files (x86)\\SmallSoft\\Small Commerce"
    elif sistema_emissor == "Comercial":
        resposta = messagebox.askyesno("Escolha", f"Sistema selecionado {sistema_emissor}\nQuer usar a pasta padrão")
        caminho = "C:\\Comercial"

    if resposta:
        return caminho
    else:
        return selecionar_pasta()

# --- Inicia a compactação --- #
def iniciar_compactacao(origem,
                        destino_zip,
                        mes_desejado,
                        ano_desejado,
                        filial):
    t = threading.Thread(
        target=compactar,
        args=(origem,
              destino_zip,
              mes_desejado,
              ano_desejado,
              filial,
              resultado),
        daemon=True
    )
    t.start()
    t.join()
    return resultado["arquivo"]

dados.gerar_chave()


dados.open_key()

def selecionar_arquivo():
    # Define o caminho padrão expandindo o $USER atual do sistema de forma segura
    # No Linux/Mac, isso aponta para /home/usuario/Documentos (ou Documentos com "D" maiúsculo)
    diretorio_padrao = os.path.expanduser("~/Documentos")

    # Se a pasta "Documentos" em português não existir, tenta em inglês ou usa a Home
    if not os.path.exists(diretorio_padrao):
        diretorio_padrao = os.path.expanduser("~/Documents")
    if not os.path.exists(diretorio_padrao):
        diretorio_padrao = os.path.expanduser("~")

    # Abre o seletor focado em arquivos .txt
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo do Telegram",
        initialdir=diretorio_padrao,
        filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )

    if arquivo:  # Se o usuário não cancelar
        token, chat_id = carregar_texto(arquivo)
        return token, chat_id
    else:
        token, chat_id = carregar_texto("")
        return token, chat_id

def carregar_texto(arquivo):

    if os.path.isfile(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            texto = f.read()
            paragrafo = texto.split("\n")
            telegram_token = paragrafo[0].split("=")
            telegram_chat_id = paragrafo[1].split("=")
            dados.gravar_dados("telegrambot", telegram_token[1])
            dados.gravar_dados("chat_id", telegram_chat_id[1])
    else:
        messagebox.showerror("Erro", f"Arquivo não encontrado: {arquivo}")

    return telegram_token[1], telegram_chat_id[1]


# Exemplo de uso:
#origem = r"C:\Users\yannick\Documents\projeto"   # pasta de origem
#destino = r"C:\Users\yannick\Desktop\projeto.zip" # arquivo ZIP de destino

#compactar_pasta(origem, destino)
