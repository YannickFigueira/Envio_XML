import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pathlib import Path

import metodos, verificarversao, xmlreadnota, transferarea
import platform, os

from pystray import Icon, MenuItem, Menu
from PIL import Image

agora = datetime.now()
dia = agora.strftime("%d")
mes = agora.strftime("%m")
ano = agora.strftime("%Y")

pad_x = 10
pad_y = 5

if platform.system() == "Windows":
    destino_dir = "C:\\temp\\XMLs"
    if not os.path.exists(destino_dir):
        os.makedirs(destino_dir)
elif platform.system() == "Linux":
    destino_dir = "/tmp/XMLs"
    if not os.path.exists(destino_dir):
        os.makedirs(destino_dir)

def iniciar_janela(version, repo):
    if int(dia) > 7:
        metodos.dados.gravar_dados("executado", "False")

    ### Configuração da janela
    def esconder_janela():
        root.withdraw()

    def restaurar_janela():
        root.deiconify()

    def fechar_programa(icon):
        root.destroy()
        icon.stop()
        sys.exit()

    def preparar_xmls(mes_desejado, ano_desejado):
        smallsoft = "C:\\Program Files (x86)\\SmallSoft\\Small Commerce"


        if mes_desejado == 1:
            mes_desejado = 12
            ano_desejado -= 1
        else:
            mes_desejado -= 1

        mes_str = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro",
               "Novembro", "Dezembro"]

        caminho_danfe = f"{metodos.dados.ler_dados('caminho')}"
        caminho_nfce = ""
        if metodos.dados.ler_dados('sistema_emissor') == "SmallSoft":
            caminho_danfe = f"{metodos.dados.ler_dados('caminho')}\\xmldestinatario"
            caminho_nfce = f"{metodos.dados.ler_dados('caminho')}\\xmldestinatario\\NFCE"


        # Nota DANFE
        caminho = metodos.copiar_xmls(caminho_danfe, destino_dir,
                                      metodos.dados.ler_dados('cliente'), mes_desejado, ano_desejado)
        if caminho != "":
            if checkbox_relatorio.get():
                xmlreadnota.ler_dados_notas(caminho, "", metodos.dados)

        # Nota NFCE
        path = Path(caminho_nfce)
        if path.exists() and caminho_nfce != "":
            metodos.copiar_xmls(caminho_nfce, destino_dir,
                                      metodos.dados.ler_dados('cliente'), mes_desejado, ano_desejado)
            if caminho != "":
                if checkbox_relatorio.get():
                    xmlreadnota.ler_dados_notas(f"{caminho}", "/NFCE/", metodos.dados)


            destino_zip = metodos.iniciar_compactacao(caminho, destino_dir, mes_desejado, ano_desejado)
            if metodos.dados.ler_dados('modoenvio') == "Telegram":
                # reativar ao finalizar o funcionamento
                metodos.telegrambot.enviar_arquivo(metodos.dados.ler_dados('telegrambot'), metodos.dados.ler_dados('chat_id'), destino_zip)
                #metodos.enviar_email()
        else:
            if modo_envio_cb["values"][0] == "Telegram":
                metodos.telegrambot.enviar_mensagem(metodos.dados.ler_dados('telegrambot'), metodos.dados.ler_dados('chat_id'),f"{ano_desejado} - {mes_str[mes_desejado - 1]} - {metodos.dados.ler_dados('cliente')}\nNenhum XML gerado")

        metodos.dados.gravar_dados("executado", "True")

    def executar_acao(resposta):
        if resposta:
            preparar_xmls(int(mes), int(ano))

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
            metodos.log_mensagem("Sistema não suportado")
    def reset_telegram():
        metodos.dados.gravar_dados("telegrambot", "")
        metodos.dados.gravar_dados("chat_id", "")
        messagebox.showinfo("Completo", "Dados apagados com sucesso!")

    def alterar_dados():
        alterar = tk.Tk()
        alterar.title("Alterar Dados")
        linha = 0

        alterar.resizable(False, False)

        label_ano = ttk.Label(alterar, text="Ano da nota:")
        label_ano.grid(row=linha, column=0, padx=pad_x, pady=pad_y, sticky="w")

        ent_ano = ttk.Entry(alterar, width=25)
        ent_ano.grid(row=linha, column=1, padx=pad_x, pady=pad_y, sticky="we")
        linha += 1

        lbl_mes = ttk.Label(alterar, text="mês da nota:")
        lbl_mes.grid(row=linha, column=0, padx=pad_x, pady=pad_y, sticky="w")

        ent_mes = ttk.Entry(alterar, width=25)
        ent_mes.grid(row=linha, column=1, padx=pad_x, pady=pad_y, sticky="we")
        linha += 1

        btn_executar = ttk.Button(alterar, text="Reenviar notas",
                                   command=lambda: (preparar_xmls(int(ent_mes.get()) + 1, int(ent_ano.get())), alterar.quit()))
        btn_executar.grid(row=linha, column=0, columnspan=4, padx=pad_x, pady=pad_y, sticky="we")

        alterar.mainloop()



    # Menu Config
    menu_config = tk.Menu(barra_menu, tearoff=0)
    menu_config.add_command(label="Reenviar notas", command=alterar_dados)
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
    barra_menu.add_command(label="Sair", command=esconder_janela)
    ### Fim da barra de menu

    # Variáveis
    largura_entradas = 25
    linha = 0

    root.title(f"{title} {version}")
    """if platform.system() == "Windows":
        root.iconbitmap("imagens/xml.ico")
    elif platform.system() == "Linux":
        icon = tk.PhotoImage(file="imagens/xml.png")
        root.iconphoto(True, icon)"""
    root.resizable(False, False)
    # Redefine o comportamento do botão de fechar
    root.protocol("WM_DELETE_WINDOW", esconder_janela)
    root.withdraw()

    label_cliente = ttk.Label(root, text="Cliente:")
    label_cliente.grid(row=linha, column=0, padx=pad_x, pady=pad_y, sticky="w")

    entrada_cliente = ttk.Entry(root, width=largura_entradas)
    entrada_cliente.grid(row=linha, column=1, padx=pad_x, pady=pad_y,sticky="w")
    linha += 1

    label_email = ttk.Label(root, text="E-mail cliente:")
    label_email.grid(row=linha, column=0, padx=pad_x, pady=pad_y, sticky="w")

    entrada_email = ttk.Entry(root, width=largura_entradas)
    entrada_email.grid(row=linha, column=1, padx=pad_x, pady=pad_y, sticky="w")

    label_senha = ttk.Label(root, text="senha:")
    label_senha.grid(row=linha, column=2, padx=pad_x, pady=pad_y, sticky="w")

    entrada_senha = ttk.Entry(root, width=15, show="*")
    entrada_senha.grid(row=linha, column=3, padx=pad_x, pady=pad_y, sticky="we")
    linha += 1

    ttk.Label(root, text="Sistema emissor:").grid(row=linha, column=0, padx=pad_x, pady=pad_y, sticky="w")
    sistema_cb = ttk.Combobox(root, width=15, takefocus=False, state="readonly")
    sistema_cb.grid(row=linha, column=1, padx=pad_x, pady=pad_y, sticky="ew")
    sistema_cb["values"] = ["SmallSoft", "Outro"]
    sistema_cb.current(0)

    ttk.Label(root, text="Modo de envio:").grid(row=linha, column=2, padx=pad_x, pady=pad_y, sticky="w")
    modo_envio_cb = ttk.Combobox(root, width=15, takefocus=False, state="readonly")
    modo_envio_cb.grid(row=linha, column=3, padx=pad_x, pady=pad_y, sticky="ew")
    modo_envio_cb["values"] = ["Telegram"]
    modo_envio_cb.current(0)
    linha += 1

    label_caminho = ttk.Label(root, text="Caminho do sistema:")
    label_caminho.grid(row=linha, column=0, padx=pad_x, pady=pad_y, sticky="w")

    button_selecionar_origem = ttk.Button(root, text="Selecionar pasta do sistema de notas", command=lambda: (entrada_caminho.delete(0, "end"),
                                                                                  entrada_caminho.insert(0, metodos.verificar_sistema(sistema_cb.get()))))
    button_selecionar_origem.grid(row=linha, column=1, columnspan=3, padx=pad_x, pady=pad_y, sticky="we")
    linha += 1

    entrada_caminho = ttk.Entry(root)
    entrada_caminho.grid(row=linha, column=0, columnspan=4, padx=pad_x, pady=pad_y, sticky="we")
    linha += 1

    checkbox_relatorio = tk.BooleanVar()
    checkbox_relatorio.set(metodos.dados.ler_dados('relatorio'))
    checkbox = ttk.Checkbutton(root, text="Gerar relatório:", variable=checkbox_relatorio)
    checkbox.grid(row=linha, column=0, padx=pad_x, pady=pad_y, sticky="w")
    linha += 1

    # Área de texto
    text_area = tk.Text(root, width=50, height=5)
    text_area.grid(row=linha, column=0, columnspan=4, padx=pad_x, pady=pad_y, sticky="we")
    linha += 1
    button_gravar = ttk.Button(root, text="Gravar", command = lambda: (executar_acao(metodos.gravar_dados(entrada_cliente.get().replace(" ", ""),
                                                                                            entrada_email.get().replace(" ", ""),
                                                                                            entrada_senha.get().replace(" ", ""),
                                                                                            entrada_caminho.get(),
                                                                                            text_area.get("1.0", tk.END),
                                                                                                          modo_envio_cb.get(),
                                                                                                          sistema_cb.get())    )))
    button_gravar.grid(row=linha, column=0, columnspan=4, padx=pad_x, pady=pad_y, sticky="we")
    linha += 1

    # Inicialização
    def carregar_dados():
        entrada_cliente.delete(0, tk.END)
        entrada_cliente.insert(0, metodos.dados.ler_dados('cliente'))
        entrada_email.delete(0, tk.END)
        entrada_email.insert(0, metodos.dados.ler_dados('email'))
        entrada_senha.delete(0, tk.END)
        entrada_senha.insert(0, metodos.dados.ler_dados('senha'))
        entrada_caminho.delete(0, tk.END)
        entrada_caminho.insert(0, metodos.dados.ler_dados('caminho'))
        text_area.delete("1.0", tk.END)
        text_area.insert("1.0", "\n".join(metodos.dados.ler_dados('emailsparaenvio')))

    carregar_dados()

    # Carregar ícone (use um PNG)
    image = Image.open("imagens/xml.png")

    # Criar menu da bandeja
    menu = Menu(
        MenuItem("Configurações", restaurar_janela),
        MenuItem("Fechar", fechar_programa)
    )

    # Criar ícone na bandeja
    icon_tray = Icon("EnvioXML", image, "Envio XML", menu)

    def run_icon():
        icon_tray.run()

    threading.Thread(target=run_icon, daemon=True).start()

    ## Colocar if para verificar o dia de execução
    if not metodos.dados.ler_dados('caminho') == "":
        if not metodos.dados.ler_dados('executado') and int(dia) <= metodos.dados.ler_dados('dia'):
            preparar_xmls(int(mes), int(ano))
    else:
        root.deiconify()

    ### Desenvolvimento
    entrada_email.config(state="disabled")
    entrada_senha.config(state="disabled")
    text_area.config(state="disabled")

    transferarea.ClipboardMenu(root, entrada_caminho)
    transferarea.ClipboardMenu(root, entrada_cliente)
    transferarea.ClipboardMenu(root, entrada_email)
    transferarea.ClipboardMenu(root, entrada_senha)

    root.mainloop()
    ### FIM da janela