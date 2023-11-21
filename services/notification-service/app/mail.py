import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logging import getLogger
import smtplib

logger = getLogger("notification-service")


class Mail:
    def __init__(self, smtp_username, smtp_password, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

        try:
            self.server = smtplib.SMTP(smtp_server, smtp_port)
            self.server.starttls()
            self.server.login(smtp_username, smtp_password)
            logger.info("Соединение с сервером установлено")
        except Exception as e:
            logger.error(f"Ошибка при подключении к серверу: {e}")

    def send_message(self, subject, message, recipient_mail):
        try:
            body = f"From: {self.smtp_username}\nTo: {recipient_mail}\nSubject: {subject}\n\n{message}"
            self.server.sendmail(self.smtp_username, recipient_mail, body)
            logger.info("Сообщение отправлено успешно.")
            return True  # Добавлено возвращаемое значение
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")
            return False