import unittest
from unittest.mock import MagicMock
from app.mail import Mail
from app.config import Config, load_config

cfg: Config = load_config()

class TestMail(unittest.TestCase):
    def setUp(self):
        smtp_mock = MagicMock()
        smtp_mock.starttls.return_value = None

        with unittest.mock.patch('smtplib.SMTP', return_value=smtp_mock):
            self.mail = Mail(
                smtp_username=cfg.EMAIL_LOGIN,
                smtp_password=cfg.EMAIL_PASSWORD,
                smtp_server=cfg.SMTP_SERVER,
                smtp_port=cfg.SMTP_PORT
            )

        self.recipient_email = 'recipient@example.com'

    def test_mail_initialization(self):
        smtp_mock = MagicMock()
        smtp_mock.starttls.return_value = None

        with unittest.mock.patch('smtplib.SMTP', return_value=smtp_mock):
            mail = Mail(
                smtp_username=cfg.EMAIL_LOGIN,
                smtp_password=cfg.EMAIL_PASSWORD,
                smtp_server=cfg.SMTP_SERVER,
                smtp_port=cfg.SMTP_PORT
            )

            self.assertTrue(smtp_mock.starttls.called)
            self.assertTrue(smtp_mock.login.called)
            self.assertEqual(mail.smtp_username, cfg.EMAIL_LOGIN)
            self.assertEqual(mail.smtp_password, cfg.EMAIL_PASSWORD)
            self.assertEqual(mail.smtp_server, cfg.SMTP_SERVER)
            self.assertEqual(mail.smtp_port, cfg.SMTP_PORT)

    def test_send_message_success(self):
        subject = "Testing1"
        message = "Testing2"
        recipient_email = self.recipient_email

        result = self.mail.send_message(subject, message, recipient_email)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()