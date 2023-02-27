from fastapi import status
from app import schemas
from tests.database import client, session


def test_root(client, session):
    res = client.get("/")

    assert res.json().get("message") == "Hello World!!! - From Docker Container"
    assert res.status_code == status.HTTP_200_OK


def test_create_user(client):
    res = client.post("/users", json={
        "email": "test@example.com",
        "password": "12345"
    })

    test_user = schemas.UserOut(**res.json())

    assert res.status_code == status.HTTP_201_CREATED
    assert test_user.email == "test@example.com"
