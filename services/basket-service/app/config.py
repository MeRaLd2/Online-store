from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field, Extra


class Config(BaseSettings):
    POSTGRES_DSN: PostgresDsn = Field(
        default='postgresql://postgres:1023@postgresql:5432/postgres',
        env='POSTGRES_DSN',
        alias='POSTGRES_DSN'
    )

    PRODUCT_ENTRYPOINT: str = Field(
        default='http://localhost:5007/bakets/',
        env='PRODUCT_ENTRYPOINT',
        alias='PRODUCT_ENTRYPOINT'
    )

    RABBITMQ_DSN: AmqpDsn = Field(
        default='amqp://guest:guest@localhost//',
        env='RABBITMQ_DSN',
        alias='RABBITMQ_DSN'
    )

    QUEUE_NAME: str = Field(
        default='notification',
        env='QUEUE_NAME',
        alias='QUEUE_NAME'
    )

    EXCHANGE_NAME: str = Field(
        default='notification',
        env='EXCHANGE_NAME',
        alias='EXCHANGE_NAME'
    )

    class Config:
        env_file = ".env"  # Указываем имя файла .env
        extra = Extra.allow  # Разрешаем дополнительные входные данные

# Создаем экземпляр конфигурации
def load_config() -> Config:
    return Config()

