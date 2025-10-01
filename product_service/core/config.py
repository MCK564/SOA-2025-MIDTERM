from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    INTERNAL_SECRET: str
    DATABASE_URL: str

    class Config:
        env_file = "product_service/.env"

settings = Settings()