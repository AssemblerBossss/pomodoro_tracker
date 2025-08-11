from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "0.0.0.0"
    DB_PORT: int = 7777
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "pomodoro"
    DB_NAME: str = "pomodoro"
    DB_DRIVER: str = "postgresql+psycopg2"

    CACHE_HOST: str = "0.0.0.0"
    CACHE_PORT: int = 14000
    CACHE_DB: int = 0


    @property
    def db_url(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
