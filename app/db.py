from sqlmodel import SQLModel, Session, create_engine, text
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
    """Should not be used in production environment"""
    SQLModel.metadata.create_all(engine)

def test_engine_connectivity():
    try: 
        conn = engine.connect()
        _ = conn.execute(text('SELECT 1'))
        print('\n\n ✅ Successfully connceted to database!')
    except Exception as e:
        print('\n\n ❗️ Connection to database failed!')
        raise e

    


def get_session():
    with Session(engine) as session:
        yield session
