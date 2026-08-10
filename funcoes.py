import inspect
import logging
import os
import shutil
import subprocess
import sys
import threading
import tkinter as tk
import zipfile
from datetime import datetime
from pathlib import Path
from platform import system
from tkinter import messagebox, filedialog
from PIL import Image
from pystray import Icon, Menu, MenuItem

# Módulos próprios
import dados_tinydb, estilo, separar_notas, telegrambot, verificarversao, xmlreadnota, transferarea
from janela_alterar_dados import JanelaAlterarDados

# --- Registro de erros ---
home_dir = os.path.expanduser('~')
system = system()
if system == 'Linux':
    if not os.path.exists(f"{home_dir}/log"):
        os.mkdir(f"{home_dir}/log")

    logging.basicConfig(
        filename=f"{home_dir}/log/envio_xml.log",        # nome do arquivo
        level=logging.ERROR,         # nível de log
        format="%(asctime)s - %(levelname)s - %(message)s")

    destino_dir = "/tmp/XMLs"
    if not os.path.exists(destino_dir):
        os.makedirs(destino_dir)
elif system == 'Windows':
    if not os.path.exists(f"c:/temp"):
        os.mkdir(f"c:/temp")

    logging.basicConfig(
        filename="c:/temp/envio_xml.log",  # nome do arquivo
        level=logging.ERROR,  # nível de log
        format="%(asctime)s - %(levelname)s - %(message)s")

    destino_dir = "C:\\temp\\XMLs"
    if not os.path.exists(destino_dir):
        os.makedirs(destino_dir)

# --- Variáveis globais ---
agora = datetime.now()
dia = agora.strftime("%d")
mes = agora.strftime("%m")
ano = agora.strftime("%Y")
config_dados = dados_tinydb.carregar_dados()
# --- Comandos dos Menus da janela principal ---
def abrir_janela_alterar_dados(janela_principal):
    visual = JanelaAlterarDados(janela_principal)
    logica = Funcoes(visual)

def reset_telegram():
    resposta = messagebox.askyesno("Verificar", "Deseja mesmo deletar os dados")

    if resposta:
        dados_tinydb.atualizar_dados('telegrambot', '')
        dados_tinydb.atualizar_dados('chat_id', '')
        messagebox.showinfo("Completo", "Dados apagados com sucesso!")

def abrir_logs(): # Padronizar logs
    if system == "Windows":
        arquivo = f"C:\\{estilo.NOME_PROGRAMA}\\doc\\CHANGELOG.md"
        subprocess.run(["notepad", arquivo])
    elif system == "Linux":
        arquivo = f"/usr/share/doc/{estilo.NOME_PROGRAMA}/CHANGELOG.md"
        subprocess.run(["xdg-open", arquivo])  # ou "gedit"
    else:
        log_mensagem("Sistema não suportado")

def visitar_site():
    pagina = f"https://github.com/YannickFigueira"
    resposta = messagebox.askyesno("Sobre", f"{estilo.NOME_PROGRAMA} {estilo.VERSION}\n"
                                            f"Deseja visitar a página\n"
                                            f"Desenvolvedor YannickFigueira\n"
                                            f"chronostimeinchain@gmail.com")
    if resposta:
        verificarversao.webbrowser.open(pagina)

# --- Comandos gerais ---

def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione uma pasta")
    if pasta:  # se o usuário não cancelar
        return pasta
    else:
        return ""

def log_mensagem(msg):
    frame = inspect.currentframe().f_back

    if frame is not None:
        linha = frame.f_lineno
        arquivo = frame.f_code.co_filename
        print(f"{msg} (arquivo: {arquivo}, linha: {linha})")
    else:
        # Fallback caso não encontre o frame anterior (ex: chamado do escopo global)
        print(f"{msg} (arquivo: desconhecido, linha: desconhecida)")

# --- Inicio da classe Funções
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
            dados_tinydb.atualizar_dados('telegrambot', telegram_token[1])
            dados_tinydb.atualizar_dados('chat_id', telegram_chat_id[1])
    else:
        messagebox.showerror("Erro", f"Arquivo não encontrado: {arquivo}")

    return telegram_token[1], telegram_chat_id[1]

# --- Inicia a compactação --- #
resultado = {}
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

def compactar(origem, destino_zip, mes_desejado, ano_desejado, filial, out):
    if not origem == "":
        pasta_origem = Path(origem)
        if pasta_origem.is_dir() or pasta_origem.is_file():
            if not destino_zip == "":
                if system == 'Linux':
                    destino_zip = f"{destino_zip}/{ano_desejado}_{estilo.MES_STR[mes_desejado - 1]}_{config_dados['database']['cliente']}{filial}.zip"
                elif system == 'Windows':
                    destino_zip = f"{destino_zip}\\{ano_desejado}_{estilo.MES_STR[mes_desejado - 1]}_{config_dados['database']['cliente']}{filial}.zip"
                # Cria o arquivo ZIP no destino

                with zipfile.ZipFile(destino_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    # Percorre todos os arquivos da pasta de origem
                    contador = 0
                    # Conta todos os arquivos dentro da pasta origem
                    # total = sum(len(arquivos) for _, _, arquivos in os.walk(origem))

                    # Garante que 'origem' seja uma string se ela vier como bytes
                    if isinstance(origem, bytes):
                        origem = origem.decode('utf-8')  # ou 'latin-1' / 'cp1252' dependendo do seu SO

                    for raiz, _, arquivos in os.walk(origem):
                        for arquivo in arquivos:

                            try:
                                caminho_completo = Path(raiz) / arquivo
                                caminho_relativo = caminho_completo.relative_to(origem)
                                zipf.write(caminho_completo, caminho_relativo)

                                # atualizar_barra(contador, total, progress_canvas)
                                contador += 1
                            except Exception as e:
                                logging.error(f"Erro ao compactar {caminho_completo}: {e}")

                shutil.rmtree(origem)
                # atualizar_barra(total, total, progress_canvas)
                # messagebox.showinfo("Completo", "Finalizado com exito.")
            # else:
            # messagebox.showinfo("Verificar", "Digite algo ou selecione uma pasta.")
        # else:
        # messagebox.showinfo("Verificar", "Arquivo ou pasta inexistente")
    # else:
    # messagebox.showinfo("Verificar", "Digite algo ou selecione uma pasta")

    out["arquivo"] = destino_zip


def copiar_xmls(origem, cliente, mes_desejado, ano_desejado):
    global destino_dir_copia
    destino_compactar = ""
    if config_dados['database']['sistema_emissor'] == "SmallSoft":
        dir_nfce = f"\\nfce"
    else:
        dir_nfce = ""

    if system == "Windows":
        destino_compactar = f"{destino_dir}\\{ano_desejado}_{mes_desejado}_{cliente}"
        destino_dir_copia = f"{destino_dir}\\{ano_desejado}_{mes_desejado}_{cliente}\\notas{dir_nfce}"

        if isinstance(destino_dir_copia, bytes):
            destino_dir_copia = destino_dir_copia.decode('utf-8')

        if not os.path.exists(destino_dir_copia):
            os.makedirs(destino_dir_copia)
            if not os.path.exists(f"{destino_compactar}\\relatorio"): os.makedirs(f"{destino_compactar}\\relatorio")
    elif system == "Linux":
        destino_compactar = f"{destino_dir}/{ano_desejado}_{mes_desejado}_{cliente}"
        destino_dir_copia = f"{destino_dir}/{ano_desejado}_{mes_desejado}_{cliente}/notas"

        if isinstance(destino_dir_copia, bytes):
            destino_dir_copia = destino_dir_copia.decode('utf-8')

        if not os.path.exists(destino_dir_copia):
            os.makedirs(destino_dir_copia)
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
                if isinstance(caminho_arquivo, bytes):
                    caminho_arquivo = caminho_arquivo.decode('utf-8')

                qtd_arquivos = True
                shutil.copy2(caminho_arquivo, destino_dir_copia)

    if qtd_arquivos:
        return qtd_arquivos
    else:
        shutil.rmtree(destino_compactar)
        return False


class Funcoes:
    def __init__(self, view):
        self.view = view
        # O controlador se adapta automaticamente baseando-se em qual janela o chamou
        if hasattr(view, 'nome_janela'):
            if view.nome_janela == "janela-principal":
                self._vincular_janela_principal()
            elif view.nome_janela == "janela-alterar-dados":
                self._vincular_janela_alterar_dados()

    def _vincular_janela_principal(self):
        # --- Inicialização da janela principal ---
        dados_tinydb.gerar_chave(config_dados) # Cria a chave crypto se não existir

        if int(dia) > 7:
            dados_tinydb.atualizar_dados('executado', False)

        if not config_dados['database']['caminho_sistema'] == "":
            if not config_dados['database']['executado'] and int(dia) <= config_dados['database']['dia']:
                self.preparar_xmls(int(mes), int(ano))
        else:
            self.view.controles['janela_principal'].deiconify()

        if Path(estilo.SMALL_COMMERCE).exists():
            self.view.controles['sistema_cb'].current(0)
        elif Path(estilo.COMERCIAL).exists():
            self.view.controles['sistema_cb'].current(1)
        else:
            self.view.controles['sistema_cb'].current(0)

        # Carregar ícone (use um PNG)
        image = Image.open("imagens/xml.png")

        # Criar menu da bandeja
        menu = Menu(
            MenuItem("Configurações", self.restaurar_janela),
            MenuItem("Fechar", self.fechar_programa)
        )

        # Criar ícone na bandeja
        icon_tray = Icon("EnvioXML", image, "Envio XML", menu)

        def run_icon():
            icon_tray.run()

        threading.Thread(target=run_icon, daemon=True).start()

        def carregar_dados():
            self.view.controles['entrada_cliente'].delete(0, tk.END)
            self.view.controles['entrada_cliente'].insert(0, config_dados['database']['cliente'])
            self.view.controles['entrada_email'].delete(0, tk.END)
            self.view.controles['entrada_email'].insert(0, config_dados['database']['email'])
            self.view.controles['entrada_senha'].delete(0, tk.END)
            self.view.controles['entrada_senha'].insert(0, config_dados['database']['senha_email'])
            self.view.controles['entrada_caminho'].delete(0, tk.END)
            self.view.controles['entrada_caminho'].insert(0, config_dados['database']['caminho_sistema'])
            if not config_dados['database']['sistema_emissor'] == "":
                self.view.controles['sistema_cb'].set(config_dados['database']['sistema_emissor'])
            self.view.controles['text_area'].delete("1.0", tk.END)
            self.view.controles['text_area'].insert("1.0", f"{config_dados['database']['emails_para_envio']}")
            self.view.controles['checkbox_relatorio'].set(config_dados['database']['relatorio'])
            self.view.controles['checkbox_sistema'].set(config_dados['database']['segundo_sistema'])

        carregar_dados()

        ### Desenvolvimento
        self.view.controles['entrada_email'].config(state="disabled")
        self.view.controles['entrada_senha'].config(state="disabled")
        self.view.controles['text_area'].config(state="disabled")

        transferarea.ClipboardMenu(self.view.controles['janela_principal'], self.view.controles['entrada_caminho'])
        transferarea.ClipboardMenu(self.view.controles['janela_principal'], self.view.controles['entrada_cliente'])
        transferarea.ClipboardMenu(self.view.controles['janela_principal'], self.view.controles['entrada_email'])
        transferarea.ClipboardMenu(self.view.controles['janela_principal'], self.view.controles['entrada_senha'])

        # --- Controles do Menu ---
        # Manu config
        self.view.controles['menu_config'].add_command(label="Reenviar notas",
                                                       command=lambda: abrir_janela_alterar_dados(self.view.controles['janela_principal']))
        self.view.controles['menu_config'].add_command(label="Resetar dados Telegram", command=lambda: reset_telegram())
        # Menu ajuda
        self.view.controles['menu_ajuda'].add_command(label="Verificar atualização",
                               command=lambda: verificarversao.consultar_lancamento(estilo.REPO, estilo.VERSION))
        self.view.controles['menu_ajuda'].add_command(label="Notas da versão", command=lambda: abrir_logs())
        self.view.controles['menu_ajuda'].add_command(label="Sobre",
                                                      command=lambda: visitar_site())

        # --- Controles da janela principal ---
        self.view.controles['janela_principal'].protocol("WM_DELETE_WINDOW", self.esconder_janela)
        self.view.controles['button_selecionar_origem'].config(command=lambda: self.verificar_sistema())
        self.view.controles['button_gravar'].config(command=lambda: self.gravar_config())

    def _vincular_janela_alterar_dados(self):
        self.view.controles['btn_executar'].config(command=lambda: self.reenviar_xmls())

    ### Configuração da janela
    def esconder_janela(self):
        self.view.controles['janela_principal'].withdraw()

    def restaurar_janela(self):
        self.view.controles['janela_principal'].deiconify()

    def fechar_programa(self, icon):
        self.view.controles['janela_principal'].destroy()
        icon.stop()
        sys.exit()

    # --- Manipulação dos dados
    def verificar_sistema(self):
        sistema_emissor = self.view.controles['sistema_cb'].get()
        resposta = False
        caminho = ""
        if sistema_emissor == "SmallSoft":
            resposta = messagebox.askyesno("Escolha",
                                           f"Sistema selecionado {sistema_emissor}\nQuer usar a pasta padrão")
            caminho = "C:\\Program Files (x86)\\SmallSoft\\Small Commerce"
        elif sistema_emissor == "Comercial":
            resposta = messagebox.askyesno("Escolha",
                                           f"Sistema selecionado {sistema_emissor}\nQuer usar a pasta padrão")
            caminho = "C:\\Program Files (x86)\\Comercial"

        self.view.controles['entrada_caminho'].delete(0, "end")
        if resposta:
            self.view.controles['entrada_caminho'].insert(0, caminho)
        else:
            self.view.controles['entrada_caminho'].insert(0, selecionar_pasta())

    def gravar_config(self):
        global config_dados
        pasta = self.view.controles['entrada_caminho'].get()

        segundo_sistema = ""
        if self.view.controles['checkbox_sistema'].get():
            segundo_sistema = selecionar_pasta()

        entrada = ""
        if system == "Windows":
            entrada = str(pasta).replace("/", "\\")
        elif system == "Linux":
            entrada = str(pasta)
        else:
            log_mensagem("Sistema não suportado")

        caminho = Path(entrada)
        if caminho.exists() and pasta != "":
            dados_tinydb.atualizar_dados('cliente', self.view.controles['entrada_cliente'].get().strip())
            dados_tinydb.atualizar_dados('email', self.view.controles['entrada_email'].get())
            dados_tinydb.atualizar_dados('senha_email',
                                         dados_tinydb.crypto.cripto_dados(dados_tinydb.open_key(config_dados),
                                                                          self.view.controles['entrada_senha'].get()))
            dados_tinydb.atualizar_dados('caminho_sistema', pasta)
            dados_tinydb.atualizar_dados('emails_para_envio', self.view.controles['text_area'].get("1.0", tk.END))
            dados_tinydb.atualizar_dados('modo_envio', self.view.controles['modo_envio_cb'].get())
            dados_tinydb.atualizar_dados('sistema_emissor', self.view.controles['sistema_cb'].get())
            dados_tinydb.atualizar_dados('relatorio', self.view.controles['checkbox_relatorio'].get())
            dados_tinydb.atualizar_dados('segundo_sistema', self.view.controles['checkbox_sistema'].get())
            dados_tinydb.atualizar_dados('segundo_sis_pasta', segundo_sistema)
            if config_dados['database']['telegrambot'] == "":
                # token, chat_id = telegrambot.janela_telegram()
                messagebox.showinfo("Telegram", "Selecione o arquivo de configuração do Telegram")
                token, chat_id = selecionar_arquivo()
                dados_tinydb.atualizar_dados('telegrambot', dados_tinydb.crypto.cripto_dados(dados_tinydb.open_key(config_dados), token))
                dados_tinydb.atualizar_dados('chat_id', dados_tinydb.crypto.cripto_dados(dados_tinydb.open_key(config_dados), chat_id))
            config_dados = dados_tinydb.carregar_dados()
            resposta = messagebox.askyesno("Completo", "Dados gravados com sucesso!\nDeseja fazer a primeira execução?")

            if resposta:
                self.preparar_xmls(int(mes), int(ano))
                messagebox.showinfo("Concluído", "XML preparado e enviado com sucesso!")
        else:
            messagebox.showwarning("ERRO", "Pasta não existe!")

    def preparar_xmls(self, mes_desejado, ano_desejado):
        if mes_desejado == 1:
            mes_desejado = 12
            ano_desejado -= 1
        else:
            mes_desejado -= 1

        # Transforma os caminhos do config em objetos Path para manipulação segura
        caminho_base_1 = Path(config_dados['database']['caminho_sistema'])
        caminho_base_2 = Path(config_dados['database']['segundo_sis_pasta'])

        sistema = config_dados['database']['sistema_emissor']

        # Inicializa as listas vazias para preenchimento dinâmico
        caminho_danfe = []
        caminho_nfce = []

        if sistema == "SmallSoft":
            # O operador / junta as pastas sem você se preocupar com as barras \
            caminho_danfe = [
                str(caminho_base_1 / "xmldestinatario"),
                str(caminho_base_2 / "xmldestinatario")
            ]
            caminho_nfce = [
                str(caminho_base_1 / "xmldestinatario" / "NFCE"),
                str(caminho_base_2 / "xmldestinatario" / "NFCE")
            ]

        elif sistema == "Comercial":
            caminho_danfe = [
                str(caminho_base_1 / "docs"),
                str(caminho_base_2 / "docs")
            ]
            # Se o Comercial não usa NFC-e, criamos a lista vazia ou mantemos strings vazias
            caminho_nfce = ["", ""]

        contador = 1
        filial = ["", "_filial"]
        if config_dados['database']['segundo_sistema']:
            contador = 2

        for i in range(contador):
            # Nota DANFE
            encontrado_notas = copiar_xmls(caminho_danfe[i],
                                                   f"{config_dados['database']['cliente']}{filial[i]}",
                                                    mes_desejado,
                                                    ano_desejado)
            if encontrado_notas:
                if config_dados['database']['relatorio']:
                    origem_separada = f"{destino_dir}\\{ano_desejado}_{mes_desejado}_{config_dados['database']['cliente']}{filial[i]}\\notas"
                    destino_separada = f"{destino_dir}\\{ano_desejado}_{mes_desejado}_{config_dados['database']['cliente']}{filial[i]}\\canceladas"
                    separar_notas.separar_notas(origem_separada, destino_separada, "cancelada")
                    destino_contingencia = f"{destino_dir}\\{ano_desejado}_{mes_desejado}_{config_dados['database']['cliente']}{filial[i]}\\contingencia"
                    separar_notas.separar_notas(origem_separada, destino_contingencia, "contingencia")

                    xmlreadnota.ler_dados_notas(f"{destino_dir}\\{ano_desejado}_{mes_desejado}_{config_dados['database']['cliente']}{filial[i]}",
                                                "", mes_desejado, ano_desejado)

            # Nota NFCE
            path = Path(caminho_nfce[i])
            if path.exists() and caminho_nfce[i] != "":
                encontrado_notas = copiar_xmls(caminho_nfce[i],
                                                        f"{config_dados['database']['cliente']}{filial[i]}",
                                                        mes_desejado,
                                                        ano_desejado)
                if encontrado_notas:
                    if self.view.controles['checkbox_relatorio'].get():
                        xmlreadnota.ler_dados_notas(
                            f"{destino_dir}\\{ano_desejado}_{mes_desejado}_{config_dados['database']['cliente']}{filial[i]}",
                                                    "/NFCE/", mes_desejado, ano_desejado)

            destino_zip_envio = iniciar_compactacao(f"{destino_dir}\\{ano_desejado}_{mes_desejado}_{config_dados['database']['cliente']}{filial[i]}",
                                                      destino_dir,
                                                      mes_desejado,
                                                      ano_desejado,
                                                      filial[i])

            # Envio do Telegram
            telegram, chat_id = dados_tinydb.ler_dados_telegram(config_dados)
            if config_dados['database']['modo_envio'] == "Telegram" and encontrado_notas:
                telegrambot.enviar_arquivo(telegram, chat_id, destino_zip_envio)
                #metodos.enviar_email()
            else:
                if config_dados['database']['modo_envio'] == "Telegram":
                    telegrambot.enviar_mensagem(telegram, chat_id,
                                                f"{ano_desejado} -"
                                                f" {estilo.MES_STR[mes_desejado - 1]} -"
                                                f" {config_dados['database']['cliente']}\nNenhum XML gerado")

        dados_tinydb.atualizar_dados('executado', True)
    # Fim das configurações da janela principal
    # Configurações da janela alterar dados
    def reenviar_xmls(self):
        self.preparar_xmls(int(self.view.controles['ent_mes'].current()) + 2, int(self.view.controles['ent_ano'].get()))
        messagebox.showinfo("Concluído", "XML preparado e enviado com sucesso!")
        self.view.controles['janela_alterar'].destroy()