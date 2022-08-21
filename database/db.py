from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autocommit=False)

def get_test_db():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    test_engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    from .models import Base as ModelsBase
    ModelsBase.metadata.create_all(test_engine)
    return TestingSessionLocal()

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_database():
    from .models import Base as ModelsBase
    ModelsBase.metadata.create_all(engine)
