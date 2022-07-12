from pydantic import BaseSettings

# Setting class for reading secrets from .env file
class Settings(BaseSettings):
    SQL_DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_TIME: int

    class Config:
        env_file = ".env"

settings=Settings()