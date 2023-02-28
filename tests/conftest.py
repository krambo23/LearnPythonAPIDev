import pytest
from fastapi import status
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


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "user@email.com",
        "password": "123"
    }

    res = client.post("/users", json=user_data)

    assert res.status_code == status.HTTP_201_CREATED

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

