import tkinter as tk
from tkinter import ttk
import metodos
import verificarversao

root = tk.Tk()

def iniciar_janela(version, repo):
    # Variaveis
    largura_entradas = 25

    root.title(f"Envio XML {version}")
    root.resizable(False, False)

    label_cliente = ttk.Label(root, text="Cliente:")
    label_cliente.grid(row=0, column=0, padx=(10, 0), pady=(5, 8), sticky="w")

    entrada_cliente = ttk.Entry(root, width=largura_entradas)
    entrada_cliente.grid(row=0, column=1, padx=(10, 0), pady=(5, 8),sticky="w")

    label_email = ttk.Label(root, text="E-mail cliente:")
    label_email.grid(row=1, column=0, padx=(10, 0), pady=(5, 8), sticky="w")

    entrado_email = ttk.Entry(root, width=largura_entradas)
    entrado_email.grid(row=1, column=1, padx=(10, 0), pady=(5, 8), sticky="w")

    label_senha = ttk.Label(root, text="senha:")
    label_senha.grid(row=1, column=2, padx=(10, 0), pady=(5, 8), sticky="w")

    entrada_senha = ttk.Entry(root, width=15)
    entrada_senha.grid(row=1, column=3, padx=10, pady=(5, 8), sticky="w")

    label_email = ttk.Label(root, text="Caminho do sistema:")
    label_email.grid(row=2, column=0, padx=(10, 0), pady=(5, 8), sticky="w")

    entrado_email = ttk.Entry(root)
    entrado_email.grid(row=2, column=1, columnspan=3, padx=10, pady=(5, 8), sticky="we")

    # Área de texto
    text_area = tk.Text(root, width=50, height=5)
    text_area.grid(row=3, column=0, columnspan=4, padx=10, pady=(0, 8), sticky="we")

    button_gravar = ttk.Button(root, text="Gravar")
    button_gravar.grid(row=4, column=0, columnspan=4, padx=10, pady=(0, 8), sticky="we")

    # verificar versão
    button_update = ttk.Button(root, text="Verificar atualização",
                               command=lambda: verificarversao.consultar_lancamento(repo, version))
    button_update.grid(row=5, column=0, columnspan=4, padx=10, pady=(5, 8), sticky="we")

    root.mainloop()