from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    db_engine: str
    db_name: str
    postgres_user: str
    postgres_password: str
    db_host: str
    db_port: int
    database_url: str = None

    secret_key: str
    refresh_secret_key: str
    algorithm: str
    token_expired_minutes: int = 15
    refresh_token_expire_minutes: int = 600


settings = Settings()
