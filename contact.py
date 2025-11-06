import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

from db_connection import connect_to_db

load_dotenv()

def save_contact(name, email, message):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO CONTACTS (NAME, EMAIL, MESSAGE) VALUES (:1, :2, :3)"
            cursor.execute(query, (name, email, message))
            connection.commit()
            print("Contact saved successfully.")
        except Exception as error:
            print("Error saving contact:", error)
        finally:
            connection.close()


def send_contact_email(name, email, message):
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
        msg["Reply-To"] = email # permite responder diretamente para quem enviou

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)

        print("Email sent successfully.")
    except Exception as error:
        print("Error sending email:", error)


def handle_contact(name, email, message):
    save_contact(name, email, message)
    send_contact_email(name, email, message)
