import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

from db_connection import connect_to_db

load_dotenv()


def save_contact(name, email, message):
    """
    Salva dados do formulário de contato no banco de dados.
    """
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO CONTACTS (NAME, EMAIL, MESSAGE) VALUES (:1, :2, :3)"
            cursor.execute(query, (name, email, message))
            connection.commit()
            print("Contato salvo com sucesso.")
        except Exception as error:
            print("Erro ao salvar o contato:", error)
        finally:
            connection.close()


def send_contact_email(name, email, message):
    """
    Envia um e-mail de notificação com os dados do formulário
    """
    try:
        sender = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASSWORD")
        receiver = os.getenv("EMAIL_TO")

        subject = f"Fale Conosco - Nova mensagem de {name}"
        body = f"""
        Você recebeu uma nova mensagem pelo site Reaproveita

        Nome: {name}
        E-mail: {email}
        Mensagem:
        {message}

        Responder para: {email}
        """

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver
        msg["Reply-To"] = email  # permite responder diretamente para quem enviou

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)

        print("Email enviado com sucesso.")
    except Exception as error:
        print("Erro ao enviar o email:", error)


def handle_contact(name, email, message):
    """
    Processa o envio do formulário de contato.
    """
    save_contact(name, email, message)
    send_contact_email(name, email, message)
