import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox

import telegrambot
import metodos, verificarversao, xmlreadnota
import platform, os

from pystray import Icon, MenuItem, Menu
from PIL import Image



if platform.system() == "Windows":
    destino_dir = "C:\\temp\\XMLs"
    if not os.path.exists(destino_dir):
        os.makedirs(destino_dir)
elif platform.system() == "Linux":
    destino_dir = "/tmp/XMLs"
    if not os.path.exists(destino_dir):
        os.makedirs(destino_dir)

def iniciar_janela(version, repo):
    root = tk.Tk()
    title = "Envio XML"
    # Criar barra de menu
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu)

    def visitar_site():
        pagina = f"https://github.com/YannickFigueira"
        resposta = messagebox.askyesno("Sobre", f"{title} v{version}\n"
                                                f"Deseja visitar a página\n"
                                                f"Desenvolvedor YannickFigueira\n"
                                                f"chronostimeinchain@gmail.com")
        if resposta:
            verificarversao.webbrowser.open(pagina)

    def abrir_logs():
        if platform.system() == "Windows":
            arquivo = "C:\\Programa Igreja\\doc\\CHANGELOG.md"
            subprocess.run(["notepad", arquivo])
        elif platform.system() == "Linux":
            arquivo = "/usr/share/doc/programaigreja/CHANGELOG.md"
            subprocess.run(["xdg-open", arquivo])  # ou "gedit"
        else:
            print("Sistema não suportado")
    def reset_telegram():
        metodos.dados.config["database"]["telegrambot"] = ""
        metodos.dados.config["database"]["chat_id"] = ""
        messagebox.showinfo("Completo", "Dados apagados com sucesso!")

    # Menu Config
    menu_config = tk.Menu(barra_menu, tearoff=0)
    menu_config.add_command(label="Resetar dados Telegram",
                            command=lambda: reset_telegram())
    barra_menu.add_cascade(label="Configuração", menu=menu_config)

    # Menu Ajuda
    menu_ajuda = tk.Menu(barra_menu, tearoff=0)
    menu_ajuda.add_command(label="Verificar atualização",
                           command=lambda: verificarversao.consultar_lancamento(repo, version))
    menu_ajuda.add_command(label="Notas da versão",
                           command=lambda: abrir_logs())
    menu_ajuda.add_command(label="Sobre",
                           command=lambda: visitar_site())
    barra_menu.add_cascade(label="Ajuda", menu=menu_ajuda)

    # Menu Sair
    barra_menu.add_command(label="Sair", command=root.destroy)
    ### Fim da barra de menu

    # Variaveis
    largura_entradas = 25
    linha = 0

    def esconder_janela():
        root.withdraw()  # apenas esconde a janela

    root.title(f"{title} {version}")
    if platform.system() == "Windows":
        root.iconbitmap("imagens/xml.ico")
    elif platform.system() == "Linux":
        icon = tk.PhotoImage(file="imagens/xml.png")
        root.iconphoto(True, icon)
    root.resizable(False, False)
    # Redefine o comportamento do botão de fechar
    #root.protocol("WM_DELETE_WINDOW", esconder_janela)

    label_cliente = ttk.Label(root, text="Cliente:")
    label_cliente.grid(row=linha, column=0, padx=(10, 0), pady=(5, 8), sticky="w")

    entrada_cliente = ttk.Entry(root, width=largura_entradas)
    entrada_cliente.grid(row=linha, column=1, padx=(10, 0), pady=(5, 8),sticky="w")
    linha += 1

    label_email = ttk.Label(root, text="E-mail cliente:")
    label_email.grid(row=linha, column=0, padx=(10, 0), pady=(5, 8), sticky="w")

    entrada_email = ttk.Entry(root, width=largura_entradas)
    entrada_email.grid(row=linha, column=1, padx=(10, 0), pady=(5, 8), sticky="w")

    label_senha = ttk.Label(root, text="senha:")
    label_senha.grid(row=linha, column=2, padx=(10, 0), pady=(5, 8), sticky="w")

    entrada_senha = ttk.Entry(root, width=15, show="*")
    entrada_senha.grid(row=linha, column=3, padx=10, pady=(5, 8), sticky="we")
    linha += 1

    label_caminho = ttk.Label(root, text="Caminho do sistema:")
    label_caminho.grid(row=linha, column=0, padx=(10, 0), pady=(5, 8), sticky="w")

    button_selecionar_origem = ttk.Button(root, text="Selecionar pasta de XMLs", command=lambda: (entrada_caminho.delete(0, "end"),
                                                                                  entrada_caminho.insert(0,
                                                                                                        metodos.selecionar_pasta())))
    button_selecionar_origem.grid(row=linha, column=1, columnspan=3, padx=10, pady=(0, 8), sticky="we")
    linha += 1

    entrada_caminho = ttk.Entry(root)
    entrada_caminho.grid(row=linha, column=0, columnspan=4, padx=10, pady=(5, 8), sticky="we")
    linha += 1

    ttk.Label(root, text="Sistema:").grid(row=linha, column=0, padx=5, pady=5, sticky="w")
    sistema_cb = ttk.Combobox(root, width=15, takefocus=False, state="readonly")
    sistema_cb.grid(row=linha, column=1, padx=10, pady=5, sticky="ew")
    sistema_cb["values"] = ["SmallSoft"]
    sistema_cb.current(0)

    ttk.Label(root, text="Modo de envio:").grid(row=linha, column=2, padx=5, pady=5, sticky="w")
    modo_envio_cb = ttk.Combobox(root, width=15, takefocus=False, state="readonly")
    modo_envio_cb.grid(row=linha, column=3, padx=10, pady=5, sticky="ew")
    modo_envio_cb["values"] = ["Telegram"]
    modo_envio_cb.current(0)
    linha += 1

    checkbox_relatorio = tk.BooleanVar()
    checkbox_relatorio.set(metodos.dados.relatorio)
    checkbox = ttk.Checkbutton(root, text="Gerar relatório:", variable=checkbox_relatorio)
    checkbox.grid(row=linha, column=0, padx=10, pady=(0, 8), sticky="w")

    # Área de texto
    text_area = tk.Text(root, width=50, height=5)
    text_area.grid(row=linha, column=0, columnspan=4, padx=10, pady=(0, 8), sticky="we")
    linha += 1

    button_gravar = ttk.Button(root, text="Gravar", command = lambda: (metodos.gravar_dados(entrada_cliente.get(), entrada_email.get(), entrada_senha.get(), entrada_caminho.get(), text_area.get("1.0", tk.END)),
                                                                       preparar_xmls(10, 2022)
    ))
    button_gravar.grid(row=linha, column=0, columnspan=4, padx=10, pady=(0, 8), sticky="we")
    linha += 1

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
    def preparar_xmls(mes_desejado, ano_desejado):
        caminho = metodos.copiar_xmls(metodos.dados.atualizar_dados('caminho'), destino_dir,
                                                        metodos.dados.atualizar_dados('cliente'), mes_desejado, ano_desejado)
        if checkbox_relatorio.get():
            xmlreadnota.ler_dados_notas(caminho, metodos.dados)
        destino_zip = metodos.iniciar_compactacao(caminho, destino_dir, mes_desejado, ano_desejado)
        if modo_envio_cb["values"][0] == "Telegram":
            if metodos.dados.atualizar_dados('telegrambot') == "":
                token, chat_id = telegrambot.janela_telegram()
                metodos.dados.config["database"]["telegrambot"] = token
                metodos.dados.config["database"]["chat_id"] = chat_id
            else:
                print(metodos.dados.atualizar_dados('telegrambot'))
                # reativar ao finalizar o funcionamento
                #telegrambot.enviar_arquivo(metodos.dados.atualizar_dados('telegrambot'), metodos.dados.atualizar_dados('chat_id'), destino_zip)
        #metodos.enviar_email()

    root.mainloop()

def fechar_programa(icon, item):
    icon.stop()
    sys.exit()

def inciar_tray(version, repo):

    # Carregar ícone (use um PNG)
    image = Image.open("imagens/xml.png")

    # Criar menu da bandeja
    menu = Menu(
        MenuItem("Configurações", lambda icon, item: iniciar_janela(version, repo)),
        MenuItem("Fechar", fechar_programa)
    )

    # Criar ícone na bandeja
    icon = Icon("EnvioXML", image, "Envio XML", menu)
    icon.run()