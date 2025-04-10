import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


def send_alert(count, mentions):
    subject = f"⚠️ Alerta: {count} possíveis problemas com PIX detectados"
    body = "Foram detectadas as seguintes menções:\n\n"
    for mention in mentions:
        body += f"- {mention}\n"
    body += "\nAcesse o painel para mais detalhes."

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("[ALERTA ENVIADO] Email com menções de PIX enviado com sucesso.")
    except Exception as e:
        print(f"[ERRO] Falha ao enviar e-mail: {e}")