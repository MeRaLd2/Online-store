from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field, Extra

class Config(BaseSettings):
    POSTGRES_DSN: PostgresDsn = Field(
        default='postgresql://postgres:postgres@localhost:5432/postgres',
        env='POSTGRES_DSN',
        alias='POSTGRES_DSN'
    )

    FEEDBACK_SERVICE_ENTRYPOINT: str = Field(
        default='http://feedback-service:5004/',
        env='FEEDBACK_SERVICE_ENTRYPOINT',
        alias='FEEDBACK_SERVICE_ENTRYPOINT'
    )

    class Config:
        env_file = ".env"
        extra = Extra.allow

def load_config() -> Config:
    return Config()

