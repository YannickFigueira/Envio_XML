from datetime import datetime
from tkinter import ttk
import customtkinter as ctk

import estilo


class JanelaReenviar:
    def __init__(self, janela_principal):
        self.janela_reenviar = ctk.CTkToplevel(janela_principal)
        self.janela_reenviar.title("Reenviar XMLs")
        self.janela_reenviar.iconbitmap("imagens/xml.ico")
        self.janela_reenviar.resizable(False, False)

        self.nome_janela = "janela-reenviar"
        self.controles = {}

        self._criar_layout()

    def _criar_layout(self):
        # --- Variáveis dos controles ---
        linha_reenviar = 0

        # --- Controles ---
        self.janela_reenviar.grab_set()
        self.controles['janela_reenviar'] = self.janela_reenviar

        self.label_ano = ctk.CTkLabel(self.janela_reenviar, text="Ano da nota:")
        self.label_ano.grid(row=linha_reenviar, column=0, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="w")

        largura_option = 150
        # 1. Pega o ano atual do sistema de forma dinâmica
        ano_atual = datetime.now().year
        # 2. Cria a lista de anos de 2026 (ano atual) até 2000 em ordem decrescente
        # O passo -1 faz a contagem ir voltando no tempo
        anos_disponiveis = [str(ano_alterar) for ano_alterar in range(ano_atual, 2019, -1)]
        # 3. Cria o Combobox no lugar do Entry
        self.ent_ano = ctk.CTkOptionMenu(self.janela_reenviar, width=largura_option)
        self.ent_ano.grid(row=linha_reenviar, column=1, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="we")
        # 4. Define o ano atual como a opção padrão pré-selecionada (índice 0 da lista)
        self.ent_ano.configure(values=anos_disponiveis)
        self.ent_ano.set(anos_disponiveis[0])
        self.controles['ent_ano'] = self.ent_ano
        linha_reenviar += 1

        self.lbl_mes = ctk.CTkLabel(self.janela_reenviar, text="mês da nota:")
        self.lbl_mes.grid(row=linha_reenviar, column=0, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="w")

        self.ent_mes = ctk.CTkOptionMenu(self.janela_reenviar, width=largura_option)
        self.ent_mes.grid(row=linha_reenviar, column=1, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="we")
        self.ent_mes.configure(values=estilo.MES_STR)
        self.ent_mes.set(estilo.MES_STR[0])
        self.controles['ent_mes'] = self.ent_mes
        linha_reenviar += 1

        self.btn_executar = ctk.CTkButton(self.janela_reenviar, text="Reenviar notas")
        self.btn_executar.grid(row=linha_reenviar, column=0, columnspan=4, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="we")
        self.controles['btn_executar'] = self.btn_executar
