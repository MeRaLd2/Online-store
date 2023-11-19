from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field, Extra

class Config(BaseSettings):
    POSTGRES_DSN: PostgresDsn = Field(
        default='postgresql://postgres:postgres@localhost:5432/postgres',
        env='POSTGRES_DSN',
        alias='POSTGRES_DSN'
    )

    POLICY_SERVICE_ENTRYPOINT: str = Field(
        default='http://localhost:5100/',
        env='POLICY_SERVICE_ENTRYPOINT',
        alias='POLICY_SERVICE_ENTRYPOINT'
    )

    APARTMENT_SERVICE_ENTRYPOINT: str = Field(
        default='http://favorite-service:5005/',
        env='APARTMENT_SERVICE_ENTRYPOINT',
        alias='APARTMENT_SERVICE_ENTRYPOINT'
    )

    class Config:
        env_file = ".env"
        extra = Extra.allow

def load_config() -> Config:
    return Config()

