import tkinter as tk
from tkinter import ttk
import metodos, verificarversao, xmlreadnota
import platform, os

root = tk.Tk()

if platform.system() == "Windows":
    destino_dir = "C:\\temp\\XMLs"
    if not os.path.exists(destino_dir):
        os.makedirs(destino_dir)
elif platform.system() == "Linux":
    destino_dir = "/tmp/XMLs"
    if not os.path.exists(destino_dir):
        os.makedirs(destino_dir)

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

    entrada_email = ttk.Entry(root, width=largura_entradas)
    entrada_email.grid(row=1, column=1, padx=(10, 0), pady=(5, 8), sticky="w")

    label_senha = ttk.Label(root, text="senha:")
    label_senha.grid(row=1, column=2, padx=(10, 0), pady=(5, 8), sticky="w")

    entrada_senha = ttk.Entry(root, width=15, show="*")
    entrada_senha.grid(row=1, column=3, padx=10, pady=(5, 8), sticky="w")

    label_caminho = ttk.Label(root, text="Caminho do sistema:")
    label_caminho.grid(row=2, column=0, padx=(10, 0), pady=(5, 8), sticky="w")

    entrada_caminho = ttk.Entry(root)
    entrada_caminho.grid(row=3, column=0, columnspan=4, padx=10, pady=(5, 8), sticky="we")

    button_selecionar_origem = ttk.Button(root, text="Selecionar pasta de XMLs", command=lambda: (entrada_caminho.delete(0, "end"),
                                                                                  entrada_caminho.insert(0,
                                                                                                        metodos.selecionar_pasta())))
    button_selecionar_origem.grid(row=2, column=1, columnspan=3, padx=10, pady=(0, 8), sticky="we")

    # Área de texto
    text_area = tk.Text(root, width=50, height=5)
    text_area.grid(row=4, column=0, columnspan=4, padx=10, pady=(0, 8), sticky="we")

    button_gravar = ttk.Button(root, text="Gravar", command = lambda: (metodos.gravar_dados(entrada_cliente.get(), entrada_email.get(), entrada_senha.get(), entrada_caminho.get(), text_area.get("1.0", tk.END)),
                                                                       preparar_xmls()
    ))
    button_gravar.grid(row=5, column=0, columnspan=4, padx=10, pady=(0, 8), sticky="we")

    # verificar versão
    button_update = ttk.Button(root, text="Verificar atualização",
                               command=lambda: verificarversao.consultar_lancamento(repo, version))
    button_update.grid(row=6, column=0, columnspan=4, padx=10, pady=(5, 8), sticky="we")

    # Inicialização
    def carregar_dados():
        entrada_cliente.delete(0, tk.END)
        entrada_cliente.insert(0, metodos.dados.cliente)
        entrada_email.delete(0, tk.END)
        entrada_email.insert(0, metodos.dados.email)
        entrada_senha.delete(0, tk.END)
        entrada_senha.insert(0, metodos.dados.senha)
        entrada_caminho.delete(0, tk.END)
        entrada_caminho.insert(0, metodos.dados.caminho)
        text_area.delete("1.0", tk.END)
        text_area.insert("1.0", "\n".join(metodos.dados.emails))

    carregar_dados()
    def preparar_xmls():
        caminho = metodos.copiar_xmls(metodos.dados.atualizar_dados('caminho'), destino_dir,
                                                        metodos.dados.atualizar_dados('cliente'), 10, 2022)
        xmlreadnota.ler_dados_notas(caminho, metodos.dados)
        metodos.iniciar_compactacao(caminho, destino_dir)
        #metodos.enviar_email()

    root.mainloop()