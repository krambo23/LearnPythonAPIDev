from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings


SQLACHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:" \
                         f"{settings.DB_PASS}@{settings.DB_IP}:" \
                         f"{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(SQLACHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

