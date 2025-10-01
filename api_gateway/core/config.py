from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    AUTH_URL: str
    TUITION_URL: str
    PAYMENT_URL: str
    USER_URL: str
    NOTIFICATION_URL: str

    class Config:
        env_file = ".env"

settings  = Settings()