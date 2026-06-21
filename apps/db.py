#db connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#hard coded db info, will later change in production
sqlalchemy_database_url = "postgresql://postgres:admin@localhost/fastapi db"
engine = create_engine(sqlalchemy_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db(): #call function, send request, close session each time
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()