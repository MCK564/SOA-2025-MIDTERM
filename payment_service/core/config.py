from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    INTERNAL_SECRET: str
    TUITION_URL : str
    USER_URL: str
    OTP_EXPIRE_TIME : int
    REDIS_URL : str
    DATABASE_URL: str

    class Config:
        env_file = "payment_service/.env"


settings = Settings()
