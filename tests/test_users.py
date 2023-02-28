import pytest
from fastapi import status
from app import schemas
from tests.database import client, session


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

    assert res.status_code == status.HTTP_200_OK
