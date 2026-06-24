import sys
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

