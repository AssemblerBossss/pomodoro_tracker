from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from settings import Settings

settings = Settings()

engine = create_engine(settings.db_url, pool_pre_ping=True)

Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session
