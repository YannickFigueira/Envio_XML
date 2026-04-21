import tkinter as tk
from tkinter import ttk, messagebox

from telegram import Bot
import asyncio

def janela_telegram():
    root = tk.Tk()
    linha = 0

    root.title(f"Configurar Telegram")
    root.resizable(False, False)

    label_token = ttk.Label(root, text="Token:")
    label_token.grid(row=linha, column=0, padx=(10, 0), pady=(5, 8), sticky="w")

    entrada_token = ttk.Entry(root, width=50)
    entrada_token.grid(row=linha, column=1, padx=(10, 0), pady=(5, 8), sticky="we")
    linha += 1

    label_chat_id = ttk.Label(root, text="Chat ID:")
    label_chat_id.grid(row=linha, column=0, padx=(10, 0), pady=(5, 8), sticky="w")

    entrada_chat_id = ttk.Entry(root, width=50)
    entrada_chat_id.grid(row=linha, column=1, padx=(10, 0), pady=(5, 8), sticky="we")
    linha += 1

    button_update = ttk.Button(root, text="Confirmar dados",
                               command=lambda: root.quit())
    button_update.grid(row=linha, column=0, columnspan=4, padx=10, pady=(5, 8), sticky="we")

    root.mainloop()
    token = entrada_token.get()
    chat_id = entrada_chat_id.get()
    messagebox.showinfo("Completo", "Dados gravados com sucesso!")

    root.destroy()

    return token, chat_id

def enviar_arquivo(token, chat_id, caminho):
    print(caminho)

    # Token do seu bot (fornecido pelo BotFather)
    TOKEN = token

    # ID do chat (pode ser seu próprio ID ou de um grupo/canal)
    CHAT_ID = chat_id

    # Caminho do arquivo .zip
    FILE_PATH = caminho

    # Criar instância do bot
    async def enviar_arquivo():
        bot = Bot(token=TOKEN)
        with open(FILE_PATH, "rb") as f:
            await bot.send_document(chat_id=CHAT_ID, document=f)

    asyncio.run(enviar_arquivo())

    print("Arquivo enviado com sucesso!")
