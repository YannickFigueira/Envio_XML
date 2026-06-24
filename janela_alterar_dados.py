import tkinter as tk
from datetime import datetime
from tkinter import ttk

import estilo


class JanelaAlterarDados:
    def __init__(self, janela_principal):
        self.janela_alterar = tk.Toplevel(janela_principal)
        self.janela_alterar.title("Reenviar XMLs")
        self.janela_alterar.iconbitmap("imagens/xml.ico")
        self.janela_alterar.resizable(False, False)

        self.nome_janela = "janela-alterar-dados"
        self.controles = {}

        self._criar_layout()

    def _criar_layout(self):
        # --- Variáveis dos controles ---
        linha_reenviar = 0

        # --- Controles ---
        self.janela_alterar.grab_set()
        self.controles['janela_alterar'] = self.janela_alterar

        self.label_ano = ttk.Label(self.janela_alterar, text="Ano da nota:")
        self.label_ano.grid(row=linha_reenviar, column=0, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="w")

        # 1. Pega o ano atual do sistema de forma dinâmica
        ano_atual = datetime.now().year
        # 2. Cria a lista de anos de 2026 (ano atual) até 2000 em ordem decrescente
        # O passo -1 faz a contagem ir voltando no tempo
        anos_disponiveis = [str(ano_alterar) for ano_alterar in range(ano_atual, 1999, -1)]
        # 3. Cria o Combobox no lugar do Entry
        self.ent_ano = ttk.Combobox(self.janela_alterar, width=25, values=anos_disponiveis, state="readonly")
        self.ent_ano.grid(row=linha_reenviar, column=1, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="we")
        # 4. Define o ano atual como a opção padrão pré-selecionada (índice 0 da lista)
        self.ent_ano.current(0)
        self.controles['ent_ano'] = self.ent_ano
        linha_reenviar += 1

        self.lbl_mes = ttk.Label(self.janela_alterar, text="mês da nota:")
        self.lbl_mes.grid(row=linha_reenviar, column=0, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="w")

        self.ent_mes = ttk.Combobox(self.janela_alterar, width=25, values=estilo.MES_STR, state="readonly")
        self.ent_mes.grid(row=linha_reenviar, column=1, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="we")
        self.ent_mes.current(0)
        self.controles['ent_mes'] = self.ent_mes
        linha_reenviar += 1

        self.btn_executar = ttk.Button(self.janela_alterar, text="Reenviar notas")
        self.btn_executar.grid(row=linha_reenviar, column=0, columnspan=4, padx=estilo.PADX_COMPONENTE, pady=estilo.PADY_COMPONENTE, sticky="we")
        self.controles['btn_executar'] = self.btn_executar
