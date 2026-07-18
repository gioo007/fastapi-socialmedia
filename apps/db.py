#db connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

sqlalchemy_database_url = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.database_hostname}/{settings.postgres_db}"
engine = create_engine(sqlalchemy_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db(): #call function, send request, close session each time
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()