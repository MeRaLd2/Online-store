from pydantic_settings import BaseSettings

class Config(BaseSettings):
    POSTGRES_DSN: str

    class Config:
        env_file = ".env"

def load_config() -> Config:
    return Config()