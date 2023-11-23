from pydantic_settings import BaseSettings
from pydantic import Field, Extra, MongoDsn


class Config(BaseSettings):
    mongo_dsn: MongoDsn = Field(
        default='mongodb://localhost:27017/',
        env='MONGO_DSN',
        alias='MONGO_DSN'
    )

    PRODUCT_ENTRYPOINT: str = Field(
        default='http://product-service:5001/',
        env='PRODUCT_ENTRYPOINT',
        alias='PRODUCT_ENTRYPOINT'
    )

    class Config:
        env_file = ".env"  # Указываем имя файла .env
        extra = Extra.allow  # Разрешаем дополнительные входные данные

# Создаем экземпляр конфигурации
def load_config() -> Config:
    return Config()

