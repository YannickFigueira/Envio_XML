import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import platform, os
from datetime import datetime

from pystray import Icon, MenuItem, Menu
from PIL import Image

### Módulos próprios
import metodos, verificarversao, xmlreadnota, transferarea, telegrambot, separarcancelada

# Variaveis
agora = datetime.now()
dia = agora.strftime("%d")
mes = agora.strftime("%m")
ano = agora.strftime("%Y")

pad_x = 10
pad_y = 5

mes_str = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro",
               "Novembro", "Dezembro"]

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
        if mes_desejado == 1:
            mes_desejado = 12
            ano_desejado -= 1
        else:
            mes_desejado -= 1

        caminho_danfe = f"{metodos.dados.ler_dados('caminho')}"
        caminho_nfce = ""
        if metodos.dados.ler_dados('sistema_emissor') == "SmallSoft":
            caminho_danfe = f"{metodos.dados.ler_dados('caminho')}\\xmldestinatario"
            caminho_nfce = f"{metodos.dados.ler_dados('caminho')}\\xmldestinatario\\NFCE"
        elif metodos.dados.ler_dados('sistema_emissor') == "Comercial":
            caminho_danfe = f"{metodos.dados.ler_dados('caminho')}\\docs"
            caminho_nfce = ""

        contador = 1
        filial = ["", "_filial"]
        if metodos.dados.ler_dados('segundo_sistema'):
            contador = 2


        for i in range(contador):
            # Nota DANFE
            encontrado_notas = metodos.copiar_xmls(caminho_danfe,
                                                    destino_dir,
                                                   f"{metodos.dados.ler_dados('cliente')}{filial[i]}",
                                                    mes_desejado,
                                                    ano_desejado,
                                                    metodos.dados.ler_dados('sistema_emissor'))
            if encontrado_notas:
                if checkbox_relatorio.get():
                    origem_separada = f"{destino_dir}\\{ano_desejado}_{mes_desejado}_{metodos.dados.ler_dados('cliente')}{filial[i]}\\notas"
                    destino_separada = f"{destino_dir}\\{ano_desejado}_{mes_desejado}_{metodos.dados.ler_dados('cliente')}{filial[i]}\\canceladas"
                    separarcancelada.separar_notas(origem_separada, destino_separada)

                    xmlreadnota.ler_dados_notas(f"{destino_dir}\\{ano_desejado}_{mes_desejado}_{metodos.dados.ler_dados('cliente')}{filial[i]}", "", metodos.dados)

            # Nota NFCE
            path = Path(caminho_nfce)
            if path.exists() and caminho_nfce != "":
                encontrado_notas = metodos.copiar_xmls(caminho_nfce,
                                                        destino_dir,
                                                        f"{metodos.dados.ler_dados('cliente')}{filial[i]}",
                                                        mes_desejado,
                                                        ano_desejado,
                                                        metodos.dados.ler_dados('sistema_emissor'))
                if encontrado_notas:
                    if checkbox_relatorio.get():
                        xmlreadnota.ler_dados_notas(f"{destino_dir}\\{ano_desejado}_{mes_desejado}_{metodos.dados.ler_dados('cliente')}{filial[i]}", "/NFCE/", metodos.dados)

            destino_zip = metodos.iniciar_compactacao(f"{destino_dir}\\{ano_desejado}_{mes_desejado}_{metodos.dados.ler_dados('cliente')}{filial[i]}",
                                                      destino_dir,
                                                      mes_desejado,
                                                      ano_desejado,
                                                      filial[i])

            # Envio do Telegram
            if metodos.dados.ler_dados('modoenvio') == "Telegram" and encontrado_notas:
                telegrambot.enviar_arquivo(metodos.dados.ler_dados('telegrambot'), metodos.dados.ler_dados('chat_id'), destino_zip)
                #metodos.enviar_email()
            else:
                if modo_envio_cb["values"][0] == "Telegram":
                    telegrambot.enviar_mensagem(metodos.dados.ler_dados('telegrambot'), metodos.dados.ler_dados('chat_id'),f"{ano_desejado} - {mes_str[mes_desejado - 1]} - {metodos.dados.ler_dados('cliente')}\nNenhum XML gerado")

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
        resposta = messagebox.askyesno("Verificar", "Deseja mesmo deletar os dados")

        if resposta:
            metodos.dados.gravar_dados("telegrambot", "")
            metodos.dados.gravar_dados("chat_id", "")
            messagebox.showinfo("Completo", "Dados apagados com sucesso!")

    def alterar_dados():
        alterar = tk.Toplevel(root)
        alterar.title("Reenviar XMLs")
        alterar.iconbitmap("imagens/xml.ico")
        alterar.grab_set()
        linha_reenviar = 0

        alterar.resizable(False, False)

        label_ano = ttk.Label(alterar, text="Ano da nota:")
        label_ano.grid(row=linha_reenviar, column=0, padx=pad_x, pady=pad_y, sticky="w")

        # 1. Pega o ano atual do sistema de forma dinâmica
        ano_atual = datetime.now().year
        # 2. Cria a lista de anos de 2026 (ano atual) até 2000 em ordem decrescente
        # O passo -1 faz a contagem ir voltando no tempo
        anos_disponiveis = [str(ano_alterar) for ano_alterar in range(ano_atual, 1999, -1)]
        # 3. Cria o Combobox no lugar do Entry
        ent_ano = ttk.Combobox(alterar, width=25, values=anos_disponiveis, state="readonly")
        ent_ano.grid(row=linha_reenviar, column=1, padx=pad_x, pady=pad_y, sticky="we")
        # 4. Define o ano atual como a opção padrão pré-selecionada (índice 0 da lista)
        ent_ano.current(0)
        linha_reenviar += 1

        lbl_mes = ttk.Label(alterar, text="mês da nota:")
        lbl_mes.grid(row=linha_reenviar, column=0, padx=pad_x, pady=pad_y, sticky="w")

        ent_mes = ttk.Combobox(alterar, width=25, values=mes_str, state="readonly")
        ent_mes.grid(row=linha_reenviar, column=1, padx=pad_x, pady=pad_y, sticky="we")
        ent_mes.current(0)
        linha_reenviar += 1

        btn_executar = ttk.Button(alterar, text="Reenviar notas",
                                   command=lambda: renviar_xmls())
        btn_executar.grid(row=linha_reenviar, column=0, columnspan=4, padx=pad_x, pady=pad_y, sticky="we")

        def renviar_xmls():
            preparar_xmls(int(ent_mes.current()) + 2, int(ent_ano.get()))
            messagebox.showinfo("Concluído", "XML preparado e enviado com sucesso!")
            alterar.destroy()

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
    if platform.system() == "Windows":
        root.iconbitmap("imagens/xml.ico")
    elif platform.system() == "Linux":
        icon_xml = tk.PhotoImage(file="imagens/xml.png")
        root.iconphoto(True, icon_xml)
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

    #entrada_senha = ttk.Entry(root, width=15, show="*")
    entrada_senha = ttk.Entry(root, width=15)
    entrada_senha.grid(row=linha, column=3, padx=pad_x, pady=pad_y, sticky="we")
    linha += 1

    ttk.Label(root, text="Sistema emissor:").grid(row=linha, column=0, padx=pad_x, pady=pad_y, sticky="w")
    sistema_cb = ttk.Combobox(root, width=15, takefocus=False, state="readonly")
    sistema_cb.grid(row=linha, column=1, padx=pad_x, pady=pad_y, sticky="ew")
    sistema_cb["values"] = ["SmallSoft", "Comercial", "Outro"]
    sistema_cb.set(metodos.dados.ler_dados('sistema_emissor'))

    ttk.Label(root, text="Modo de envio:").grid(row=linha, column=2, padx=pad_x, pady=pad_y, sticky="w")
    modo_envio_cb = ttk.Combobox(root, width=15, takefocus=False, state="readonly")
    modo_envio_cb.grid(row=linha, column=3, padx=pad_x, pady=pad_y, sticky="ew")
    modo_envio_cb["values"] = ["Telegram"]
    modo_envio_cb.current(0)
    linha += 1

    label_caminho = ttk.Label(root, text="Caminho do sistema:")
    label_caminho.grid(row=linha, column=0, padx=pad_x, pady=pad_y, sticky="w")

    button_selecionar_origem = ttk.Button(root, text="Selecionar pasta do sistema de notas",
                                          command=lambda: gravar_caminho())
    button_selecionar_origem.grid(row=linha, column=1, columnspan=3, padx=pad_x, pady=pad_y, sticky="we")
    linha += 1

    def gravar_caminho():
        # 1. Busca o sistema selecionado no Combobox
        sistema = sistema_cb.get()

        # 2. Roda a sua lógica de verificação
        caminho_verificado = metodos.verificar_sistema(sistema)

        # 3. Limpa e insere no campo de entrada
        entrada_caminho.delete(0, "end")
        entrada_caminho.insert(0, caminho_verificado)

    entrada_caminho = ttk.Entry(root)
    entrada_caminho.grid(row=linha, column=0, columnspan=4, padx=pad_x, pady=pad_y, sticky="we")
    linha += 1

    checkbox_relatorio = tk.BooleanVar()
    checkbox_relatorio.set(metodos.dados.ler_dados('relatorio'))
    checkbox_rel = ttk.Checkbutton(root, text="Gerar relatório:", variable=checkbox_relatorio)
    checkbox_rel.grid(row=linha, column=0, padx=pad_x, pady=pad_y, sticky="w")

    checkbox_sistema = tk.BooleanVar()
    checkbox_sistema.set(metodos.dados.ler_dados('segundo_sistema'))
    checkbox_sis = ttk.Checkbutton(root, text="Configurar segundo sistema:", variable=checkbox_sistema)
    checkbox_sis.grid(row=linha, column=1, padx=pad_x, pady=pad_y, sticky="w")
    linha += 1

    # Área de texto
    text_area = tk.Text(root, width=50, height=5)
    text_area.grid(row=linha, column=0, columnspan=4, padx=pad_x, pady=pad_y, sticky="we")
    linha += 1
    button_gravar = ttk.Button(root, text="Gravar",
                               command = lambda: gravar_config())
    button_gravar.grid(row=linha, column=0, columnspan=4, padx=pad_x, pady=pad_y, sticky="we")
    linha += 1

    def gravar_config():
        segundo_sistema = ""
        if checkbox_sistema.get():
            segundo_sistema = metodos.selecionar_pasta()

        executar_acao(metodos.gravar_config(entrada_cliente.get(),
                                           entrada_email.get(),
                                           entrada_senha.get(),
                                           entrada_caminho.get(),
                                           text_area.get("1.0", tk.END),
                                           modo_envio_cb.get(),
                                           sistema_cb.get(),
                                           checkbox_relatorio.get(),
                                           checkbox_sistema.get(),
                                           segundo_sistema))

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
    metodos.log_mensagem("remover senha")
    #entrada_senha.insert(0, "senha")

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
    #entrada_senha.config(state="disabled")
    text_area.config(state="disabled")

    transferarea.ClipboardMenu(root, entrada_caminho)
    transferarea.ClipboardMenu(root, entrada_cliente)
    transferarea.ClipboardMenu(root, entrada_email)
    transferarea.ClipboardMenu(root, entrada_senha)

    root.mainloop()
    ### FIM da janela