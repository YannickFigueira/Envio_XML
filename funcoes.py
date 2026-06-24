import inspect
import os
import platform
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, filedialog

import dados

# --- Comandos gerais ---
def verificar_sistema(sistema_emissor):
    resposta = False
    caminho = ""
    if sistema_emissor == "SmallSoft":
        resposta = messagebox.askyesno("Escolha",
                                       f"Sistema selecionado {sistema_emissor}\nQuer usar a pasta padrão")
        caminho = "C:\\Program Files (x86)\\SmallSoft\\Small Commerce"
    elif sistema_emissor == "Comercial":
        resposta = messagebox.askyesno("Escolha",
                                       f"Sistema selecionado {sistema_emissor}\nQuer usar a pasta padrão")
        caminho = "C:\\Comercial"

    if resposta:
        return caminho
    else:
        return selecionar_pasta()

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
            dados.gravar_dados("telegrambot", telegram_token[1])
            dados.gravar_dados("chat_id", telegram_chat_id[1])
    else:
        messagebox.showerror("Erro", f"Arquivo não encontrado: {arquivo}")

    return telegram_token[1], telegram_chat_id[1]


class Funcoes:
    def __init__(self, view):
        self.view = view
        self.repo = self.view.controles['var_repo'].get()
        self.version = self.view.controles['var_version'].get()
        self.programa_title = self.view.controles['var_title'].get()

        # O controlador se adapta automaticamente baseando-se em qual janela o chamou
        if hasattr(view, 'nome_janela'):
            if view.nome_janela == "janela-principal":
                self._vincular_janela_principal()

    def _vincular_janela_principal(self):
        #self.view.controles['janela_principal'].protocol("WM_DELETE_WINDOW", self.esconder_janela)
        self.view.controles['sistema_cb'].set(dados.ler_dados('sistema_emissor'))
        self.view.controles['button_selecionar_origem'].config(command=lambda: self.gravar_caminho())
        self.view.controles['button_gravar'].config(command=lambda: self.gravar_config())


    ### Configuração da janela
    def esconder_janela(self):
        self.view.controles['janela_principal'].withdraw()

    def restaurar_janela(self):
        self.view.controles['janela_principal'].deiconify()

    def fechar_programa(self, icon):
        self.view.controles['janela_principal'].destroy()
        icon.stop()
        sys.exit()


    def gravar_caminho(self):
        # 1. Busca o sistema selecionado no Combobox
        sistema = self.view.controles['sistema_cb'].get()

        # 2. Roda a sua lógica de verificação
        caminho_verificado = verificar_sistema(sistema)

        # 3. Limpa e insere no campo de entrada
        self.view.controles['entrada_caminho'].delete(0, "end")
        self.view.controles['entrada_caminho'].insert(0, caminho_verificado)

    def gravar_config(self):
        pasta = self.view.controles['entrada_caminho'].get()

        segundo_sistema = ""
        if self.view.controles['checkbox_sistema'].get():
            segundo_sistema = selecionar_pasta()

        entrada = ""
        if platform.system() == "Windows":
            entrada = str(pasta).replace("/", "\\")
        elif platform.system() == "Linux":
            entrada = str(pasta)
        else:
            log_mensagem("Sistema não suportado")

        caminho = Path(entrada)
        if caminho.exists() and pasta != "":
            dados.gravar_dados("cliente", self.view.controles['entrada_cliente'].get())
            dados.gravar_dados("email", self.view.controles['entrada_email'].get())

            dados.gravar_dados("senhaemail", dados.crypto.cripto_dados(dados.open_key(), self.view.controles['entrada_senha'].get()))
            dados.gravar_dados("caminhopasta", pasta)
            dados.gravar_dados("emailsparaenvio", self.view.controles['text_area'].get("1.0", tk.END))
            dados.gravar_dados("modoenvio", self.view.controles['modo_envio_cb'].get())
            dados.gravar_dados("sistema_emissor", self.view.controles['sistema_cb'].get())
            dados.gravar_dados("relatorio", str(self.view.controles['checkbox_relatorio'].get()))
            dados.gravar_dados("segundo_sistema", str(self.view.controles['checkbox_sistema'].get()))
            dados.gravar_dados("segundo_sis_pasta", segundo_sistema)
            if dados.ler_dados('telegrambot') == "":
                # token, chat_id = telegrambot.janela_telegram()
                messagebox.showinfo("Telegram", "Selecione o arquivo de configuração do Telegram")
                token, chat_id = selecionar_arquivo()
                dados.gravar_dados("telegrambot", dados.crypto.cripto_dados(dados.open_key(), token))
                dados.gravar_dados("chat_id", dados.crypto.cripto_dados(dados.open_key(), chat_id))
            resposta = messagebox.askyesno("Completo", "Dados gravados com sucesso!\nDeseja fazer a primeira execução?")

            if resposta:
                preparar_xmls(int(mes), int(ano))
        else:
            messagebox.showwarning("ERRO", "Pasta não existe!")

