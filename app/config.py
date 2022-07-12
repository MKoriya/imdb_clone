from pydantic import BaseSettings

# Setting class for reading secrets from .env file
class Settings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_DB: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_TIME: int

    class Config:
        env_file = ".env"

settings=Settings()