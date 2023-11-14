import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logging import getLogger

logger = getLogger("notification-service")


class Mail():
    def __init__(self, smtp_username, smtp_password, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_username = smtp_username

        try:
            self.server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            self.server.login(smtp_username, smtp_password)

            logger.info("соединение с сервером установленно")

        except Exception as e:
            logger.error(f"Ошибка при подключении к серверу: {e}")

    def send_message(self, subject, message, recipient_email):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.smtp_username
            msg["To"] = recipient_email
            msg["Subject"] = subject

            msg.attach(MIMEText(message, "plain"))

            self.server.sendmail(self.smtp_username, recipient_email, msg.as_string())

            logger.info("Сообщение отправлено успешно.")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")