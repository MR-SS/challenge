from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

username = os.environ.get("POSTGRES_USERNAME")
password = os.environ.get("POSTGRES_PASSWORD")



# SQLALCHEMY_DATABASE_URL = f"postgresql://sajjad:sajjad@localhost:5432/coupon"
SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@db:5432/coupon"
# print (SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autocommit=False)

def get_test_db():
    SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@db:5432/test"
    test_engine = create_engine(
        SQLALCHEMY_DATABASE_URL
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
