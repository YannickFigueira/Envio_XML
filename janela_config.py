import platform
import tkinter as tk
from tkinter import ttk

import dados, estilo

class JanelaPrincipal:
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal
        self.janela_principal.title(f"{estilo.NOME_PROGRAMA} {estilo.VERSION}")
        self.janela_principal.resizable(False, False)

        self.nome_janela = "janela-principal"  # Identificador para o seu controlador
        self.controles = {}

        self._criar_layout()
        self._criar_barra_menu()

    def _criar_layout(self):
        # --- Variáveis ---
        largura_entradas = 25
        linha = 0

        # --- Controles ---
        self.controles['janela_principal'] = self.janela_principal

        self.janela_principal.title(f"{estilo.NOME_PROGRAMA} {estilo.VERSION}")
        if platform.system() == "Windows":
            self.janela_principal.iconbitmap("imagens/xml.ico")
        elif platform.system() == "Linux":
            icon_xml = tk.PhotoImage(file="imagens/xml.png")
            self.janela_principal.iconphoto(True, icon_xml)
        self.janela_principal.resizable(False, False)
        # Redefine o comportamento do botão de fechar
        self.janela_principal.withdraw()

        self.label_cliente = ttk.Label(self.janela_principal, text="Cliente:")
        self.label_cliente.grid(row=linha, column=0, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="w")

        self.entrada_cliente = ttk.Entry(self.janela_principal, width=largura_entradas)
        self.entrada_cliente.grid(row=linha, column=1, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="w")
        self.controles['entrada_cliente'] = self.entrada_cliente
        linha += 1

        self.label_email = ttk.Label(self.janela_principal, text="E-mail cliente:")
        self.label_email.grid(row=linha, column=0, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="w")

        self.entrada_email = ttk.Entry(self.janela_principal, width=largura_entradas)
        self.entrada_email.grid(row=linha, column=1, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="w")
        self.controles['entrada_email'] = self.entrada_email

        self.label_senha = ttk.Label(self.janela_principal, text="senha:")
        self.label_senha.grid(row=linha, column=2, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="w")

        self.entrada_senha = ttk.Entry(self.janela_principal, width=15, show="*")
        self.entrada_senha.grid(row=linha, column=3, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="we")
        self.controles['entrada_senha'] = self.entrada_senha
        linha += 1

        ttk.Label(self.janela_principal, text="Sistema emissor:").grid(row=linha, column=0, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="w")
        self.sistema_cb = ttk.Combobox(self.janela_principal, width=15, takefocus=False, state="readonly")
        self.sistema_cb.grid(row=linha, column=1, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="ew")
        self.sistema_cb["values"] = ["SmallSoft", "Comercial"]
        self.controles['sistema_cb'] = self.sistema_cb

        ttk.Label(self.janela_principal, text="Modo de envio:").grid(row=linha, column=2, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="w")
        self.modo_envio_cb = ttk.Combobox(self.janela_principal, width=15, takefocus=False, state="readonly")
        self.modo_envio_cb.grid(row=linha, column=3, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="ew")
        self.modo_envio_cb["values"] = ["Telegram"]
        self.modo_envio_cb.current(0)
        self.controles['modo_envio_cb'] = self.modo_envio_cb
        linha += 1

        self.label_caminho = ttk.Label(self.janela_principal, text="Caminho do sistema:")
        self.label_caminho.grid(row=linha, column=0, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="w")

        self.button_selecionar_origem = ttk.Button(self.janela_principal, text="Selecionar pasta do sistema de notas")
        self.button_selecionar_origem.grid(row=linha, column=1, columnspan=3, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="we")
        self.controles['button_selecionar_origem'] = self.button_selecionar_origem
        linha += 1

        self.entrada_caminho = ttk.Entry(self.janela_principal)
        self.entrada_caminho.grid(row=linha, column=0, columnspan=4, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="we")
        self.controles['entrada_caminho'] = self.entrada_caminho
        linha += 1

        self.checkbox_relatorio = tk.BooleanVar()
        self.checkbox_relatorio.set(dados.ler_dados('relatorio'))
        self.checkbox_rel = ttk.Checkbutton(self.janela_principal, text="Gerar relatório:", variable=self.checkbox_relatorio)
        self.checkbox_rel.grid(row=linha, column=0, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="w")
        self.controles['checkbox_relatorio'] = self.checkbox_relatorio

        self.checkbox_sistema = tk.BooleanVar()
        self.checkbox_sistema.set(dados.ler_dados('segundo_sistema'))
        self.checkbox_sis = ttk.Checkbutton(self.janela_principal, text="Configurar segundo sistema:", variable=self.checkbox_sistema)
        self.checkbox_sis.grid(row=linha, column=1, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="w")
        self.controles['checkbox_sistema'] = self.checkbox_sistema
        linha += 1

        # Área de texto
        self.text_area = tk.Text(self.janela_principal, width=50, height=5)
        self.text_area.grid(row=linha, column=0, columnspan=4, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="we")
        self.controles['text_area'] = self.text_area
        linha += 1

        self.button_gravar = ttk.Button(self.janela_principal, text="Gravar")
        self.button_gravar.grid(row=linha, column=0, columnspan=4, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="we")
        self.controles['button_gravar'] = self.button_gravar

    def _criar_barra_menu(self):
        self.barra_menu = tk.Menu(self.janela_principal)
        self.janela_principal.config(menu=self.barra_menu)

        # Menu Config
        self.menu_config = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Configuração", menu=self.menu_config)
        self.controles['menu_config'] = self.menu_config

        # Menu Ajuda
        self.menu_ajuda = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Ajuda", menu=self.menu_ajuda)
        self.controles['menu_ajuda'] = self.menu_ajuda
        ### Fim da barra de menu
