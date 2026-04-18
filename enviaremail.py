import smtplib
import ssl, os
from email.message import EmailMessage

def enviar_zip_email(servidor, porta, usuario, senha, remetente, destinatario, assunto, corpo, caminho_zip):
    # Criar a mensagem
    msg = EmailMessage()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.set_content(corpo)

    # Ler o arquivo .zip e anexar
    with open(caminho_zip, "rb") as f:
        dados = f.read()
        msg.add_attachment(
            dados,
            maintype="application",
            subtype="zip",
            filename=caminho_zip.split(os.sep)[-1]
        )

    # Conectar ao servidor SMTP e enviar
    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL(servidor, porta, context=contexto) as smtp:
        smtp.login(usuario, senha)
        smtp.send_message(msg)
        print("E-mail enviado com sucesso!")

# Exemplo de uso
if __name__ == "__main__":
    enviar_zip_email(
        servidor="smtp.gmail.com",   # servidor SMTP
        porta=465,                   # porta SSL
        usuario="seuemail@gmail.com",
        senha="suasenhaouappkey",    # use App Password se for Gmail
        remetente="seuemail@gmail.com",
        destinatario="destinatario@exemplo.com",
        assunto="Arquivo compactado",
        corpo="Segue em anexo o arquivo .zip solicitado.",
        caminho_zip=r"C:\Users\SeuUsuario\Documentos\arquivo.zip"
    )
