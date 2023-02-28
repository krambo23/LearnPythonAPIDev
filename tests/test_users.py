import pytest
from fastapi import status
from app import schemas
from jose import jwt
from app.config import settings


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


def test_login_user(client, test_user):
    res = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id_ = payload.get("user_id")
    assert test_user["id"] == id_
    assert login_res.token_type == "bearer"
    assert res.status_code == status.HTTP_200_OK
