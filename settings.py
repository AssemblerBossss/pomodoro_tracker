from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = 'postgresql+psycopg2://postgres:pomodoro@0.0.0.0:7777/pomodoro'
