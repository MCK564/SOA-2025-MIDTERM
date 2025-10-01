from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MAIL_USERNAME : str
    MAIL_PORT : int
    MAIL_PASSWORD : str
    MAIL_FROM : str
    MAIL_SERVER : str
    MAIL_STARTTLS : bool
    MAIL_SSL_TLS : bool
    KAFKA_BOOTSTRAP_SERVERS : str
    KAFKA_TOPIC : str
    KAFKA_GROUP_ID : str
    DATABASE_URL : str

    class Config:
        env_file = ".env"


settings = Settings()