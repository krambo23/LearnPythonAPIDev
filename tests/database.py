import pytest
from app.database import get_db, Base
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from fastapi.testclient import TestClient


SQLACHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:" \
                         f"{settings.DB_PASS}@{settings.DB_IP}:" \
                         f"{settings.DB_PORT}/{settings.DB_NAME}_test"

engine = create_engine(SQLACHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def session():
    print("Dropping Tables")
    Base.metadata.drop_all(bind=engine)

    print("Creating Tables")
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    def get_test_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)
