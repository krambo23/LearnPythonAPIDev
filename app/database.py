from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_user = "postgres"
db_pass = "12345"
db_ip = "127.0.0.1"
db_name = "fastapi"
SQLACHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_ip}/{db_name}"

engine = create_engine(SQLACHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

