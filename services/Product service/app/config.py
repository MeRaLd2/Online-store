from pydantic_settings import BaseSettings

class Config(BaseSettings):
    POSTGRES_DSN: str = "postgresql://postgres:1023@postgresql:5432/postgres"

    class Config:
        env_file = ".env"

def load_config() -> Config:
    return Config()