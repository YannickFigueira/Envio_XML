import inspect
import os, shutil
import platform
import threading
import zipfile
from pathlib import Path
from platform import system
from tkinter import messagebox, filedialog
import logging
from datetime import datetime
### Módulos próprios
import dados, telegrambot

# Pasta padrão dos sistemas de notas
smallsoft = "C:\\Program Files (x86)\\SmallSoft\\Small Commerce\\xmldestinatario\\NFCE"

def log_mensagem(msg):
    frame = inspect.currentframe().f_back
    linha = frame.f_lineno
    arquivo = frame.f_code.co_filename
    print(f"{msg} (arquivo: {arquivo}, linha: {linha})")

# Variáveis
home_dir = os.path.expanduser('~')
system = system()
if system == 'Linux':
    if not os.path.exists(f"{home_dir}/log"):
        os.mkdir(f"{home_dir}/log")

    logging.basicConfig(
        filename=f"{home_dir}/log/compactar.log",        # nome do arquivo
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

def copiar_xmls(origem, destino_dir, cliente, mes_desejado, ano_desejado):
    destino_compactar = ""
    if origem == smallsoft:
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
                #print(f"Arquivo {arquivo} copiado (criado em {data_modificacao})")

    if qtd_arquivos:
        return qtd_arquivos
    else:
        shutil.rmtree(destino_compactar)
        return False

resultado = {}
def compactar(origem, destino_zip, mes_desejado, ano_desejado, out):
    mes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    if not origem == "":
        pasta_origem = Path(origem)
        if pasta_origem.is_dir() or pasta_origem.is_file():
            if not destino_zip == "":
                if system == 'Linux':
                    destino_zip = f"{destino_zip}/{ano_desejado}_{mes[mes_desejado - 1]}_{dados.ler_dados('cliente')}.zip"
                elif system == 'Windows':
                    destino_zip = f"{destino_zip}\\{ano_desejado}_{mes[mes_desejado - 1]}_{dados.ler_dados('cliente')}.zip"
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
                                #print(f"{contador} / {total}")
                                contador += 1
                            except Exception as e:
                                logging.error(f"Erro ao compactar {caminho_completo}: {e}")
                        #print(f"{contador} / {len(arquivos)}")
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

def enviar_email():
    agora = datetime.now()
    dia = agora.strftime("%d")
    dia_registro = float(dados.ler_dados('dia'))

    if (float(dia) <= dia_registro) and (dados.ler_dados('executado') == False):
        log_mensagem("Dia da semana")

    #hora = agora.strftime("%H")
    #minuto = agora.strftime("%M")
    #return hora, minuto

def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione uma pasta")
    if pasta:  # se o usuário não cancelar
        return pasta
    else:
        return ""

def verificar_sistema(sistema_emissor):
    if sistema_emissor == "SmallSoft":
        resposta = messagebox.askyesno("Escolha", f"Sistema selecionado {sistema_emissor}\nQuer usar a pasta padrão")
        caminho = "C:\\Program Files (x86)\\SmallSoft\\Small Commerce"

        if resposta:
            return caminho
        else:
            return selecionar_pasta()
    else:
        return selecionar_pasta()

# --- Inicia a compactação --- #
def iniciar_compactacao(origem,
                        destino_zip,
                        mes_desejado,
                        ano_desejado):
    t = threading.Thread(
        target=compactar,
        args=(origem,
              destino_zip,
              mes_desejado,
              ano_desejado, resultado),
        daemon=True
    )
    t.start()
    t.join()
    return resultado["arquivo"]

dados.gerar_chave()

def gravar_dados(cliente, email, senha, pasta, emails, modoenvio, sistema_emissor):
    entrada = ""
    if platform.system() == "Windows":
        entrada = str(pasta).replace("/", "\\")
    elif platform.system() == "Linux":
        entrada = str(pasta)
    else:
        log_mensagem("Sistema não suportado")
    caminho = Path(entrada)
    if caminho.exists() and pasta != "":
        dados.gravar_dados("cliente", cliente)
        dados.gravar_dados("email", email)

        dados.gravar_dados("senhaemail", dados.crypto.cripto_senha(dados.open_key(), senha))
        dados.gravar_dados("caminhopasta", pasta)
        dados.gravar_dados("emailsparaenvio", emails)
        dados.gravar_dados("modoenvio", modoenvio)
        dados.gravar_dados("sistema_emissor", sistema_emissor)
        if dados.ler_dados('telegrambot') == "":
            token, chat_id = telegrambot.janela_telegram()
            dados.gravar_dados("telegrambot", token)
            dados.gravar_dados("chat_id", chat_id)
        resposta = messagebox.askyesno("Completo", "Dados gravados com sucesso!\nDeseja fazer a primeira execução?")

        return resposta
    else:
        messagebox.showwarning("ERRO", "Pasta não existe!")

dados.open_key()

# Exemplo de uso:
#origem = r"C:\Users\yannick\Documents\projeto"   # pasta de origem
#destino = r"C:\Users\yannick\Desktop\projeto.zip" # arquivo ZIP de destino

#compactar_pasta(origem, destino)
