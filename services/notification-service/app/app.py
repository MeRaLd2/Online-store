import json
import config, mail
import logging
import broker, schemas
from kombu import Message
from notifications import basket_upload


# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=2,
    format="%(levelname)-9s %(message)s"
)

# load config
cfg: config.Config = config.load_config()

logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.json()}'
)

consumer = broker.Consumer(str(cfg.RABBITMQ_DSN), str(cfg.QUEUE_NAME))

email_send = mail.Mail(cfg.EMAIL_LOGIN, cfg.EMAIL_PASSWORD, cfg.SMTP_SERVER, cfg.SMTP_PORT)

def send_email_message(body, message: Message):
    data = json.loads(body)

    reservation_data = schemas.Notification(**data)

    notification = basket_upload(reservation_data)

    email_send.send_message('Совершена покупка', notification, reservation_data.mail)


consumer.add_callback(send_email_message)

def main():
    consumer.run()

if __name__ == "__main__":
    main()