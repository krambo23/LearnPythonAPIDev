from fastapi.testclient import TestClient
from fastapi import status
from app.database import get_db, Base
from app.main import app
from app import schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings


SQLACHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:" \
                         f"{settings.DB_PASS}@{settings.DB_IP}:" \
                         f"{settings.DB_PORT}/{settings.DB_NAME}_test"

engine = create_engine(SQLACHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)


def test_root():
    res = client.get("/")

    assert res.json().get("message") == "Hello World!!! - From Docker Container"
    assert res.status_code == status.HTTP_200_OK


def test_create_user():
    res = client.post("/users", json={
        "email": "test@example.com",
        "password": "12345"
    })

    test_user = schemas.UserOut(**res.json())

    assert res.status_code == status.HTTP_201_CREATED
    assert test_user.email == "test@example.com"
