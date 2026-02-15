from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.engine import URL
from app.core import config

url_object = URL.create(
    "postgresql",
    config.settings.DatabaseUser,
    config.settings.DatabasePassword,
    config.settings.DatabaseHost,
    config.settings.DatabasePort,
    config.settings.DatabaseName,
)

engine = create_engine(url_object)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
