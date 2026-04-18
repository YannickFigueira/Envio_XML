import os
import threading
import zipfile
import dados
from pathlib import Path
from platform import system
from tkinter import messagebox, filedialog
import logging
from datetime import datetime

# Inicializar dados

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

def compactar(origem, destino_zip):
    if not origem == "":
        pasta_origem = Path(origem)
        if pasta_origem.is_dir() or pasta_origem.is_file():
            if not destino_zip == "":
                if system == 'Linux':
                    destino_zip = f"{destino_zip}/{dados.atualizar_dados('cliente')}.zip"
                elif system == 'Windows':
                    destino_zip = f"{destino_zip}\\{dados.atualizar_dados('cliente')}.zip"
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

                    #atualizar_barra(total, total, progress_canvas)
                    #messagebox.showinfo("Completo", "Finalizado com exito.")
            #else:
                #messagebox.showinfo("Verificar", "Digite algo ou selecione uma pasta.")
        #else:
            #messagebox.showinfo("Verificar", "Arquivo ou pasta inexistente")
    #else:
        #messagebox.showinfo("Verificar", "Digite algo ou selecione uma pasta")

def enviar_email():
    agora = datetime.now()
    dia = agora.strftime("%d")
    dia_registro = float(dados.dia)

    if (float(dia) <= dia_registro) and (dados.executado == False):
        print("Dia da semana")

    #hora = agora.strftime("%H")
    #minuto = agora.strftime("%M")
    #return hora, minuto

def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione uma pasta")
    if pasta:  # se o usuário não cancelar
        return pasta
    else:
        return None

### Atualiza a barra de progresso ###
def atualizar_barra(valor, total, progress_canvas):
    progress_canvas.delete("all")
    largura = int((valor / total) * progress_canvas.winfo_width())
    # desenha a barra preenchida
    progress_canvas.create_rectangle(0, 0, largura, 25, fill="green")
    # escreve a porcentagem dentro da barra
    porcentagem = (valor / total) * 100
    x = progress_canvas.winfo_width() // 2
    progress_canvas.create_text(x, 12, text=f"{porcentagem:.3f}%", fill="black", font=("Arial", 10, "bold"), anchor="center")

# --- Inicia a compactação --- #
def iniciar_compactacao(origem,
                        destino_zip):
    t = threading.Thread(
        target=compactar,
        args=(origem,
              destino_zip),
        daemon=True
    )
    t.start()

def gravar_dados(cliente, email, senha, pasta, emails):
    dados.config["database"]["cliente"] = cliente
    dados.config["database"]["email"] = email

    dados.config["database"]["senhaemail"] = dados.crypto.cripto_senha(dados.open_key(),senha)
    dados.config["database"]["caminhopasta"] = pasta
    emails_separate = emails.split("\n")
    dados.config["database"]["emailsparaenvio"].clear()
    for separate in emails_separate:
        if separate != "":
            dados.config["database"]["emailsparaenvio"].append(separate)
    #print(emails)
    dados.gravar()
    messagebox.showinfo("Completo", "Dados gravados com sucesso!")

    print(dados.cliente)
    cliente = dados.atualizar_dados("cliente")
    print(cliente)

dados.gerar_chave()

dados.open_key()

# Exemplo de uso:
#origem = r"C:\Users\yannick\Documents\projeto"   # pasta de origem
#destino = r"C:\Users\yannick\Desktop\projeto.zip" # arquivo ZIP de destino

#compactar_pasta(origem, destino)
