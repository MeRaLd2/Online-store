import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logging import getLogger, INFO, ERROR
from smtplib import SMTPException

logger = getLogger("notification-service")

class Mail:
    def __init__(self, smtp_username, smtp_password, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                logger.info("Соединение с сервером установлено")
        except SMTPException as e:
            logger.error(f"Ошибка при подключении к серверу: {e}")

    def send_message(self, subject, message, recipient_mail):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = recipient_mail
            msg['Subject'] = subject

            body = MIMEText(message)
            msg.attach(body)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.smtp_username, recipient_mail, msg.as_string())
                logger.info("Сообщение отправлено успешно.")
                return True
        except SMTPException as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")