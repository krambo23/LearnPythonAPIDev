import pytest
from fastapi import status
from app.database import get_db, Base
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.oauth2 import create_access_token
from fastapi.testclient import TestClient
from app import models


SQLACHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:" \
                         f"{settings.DB_PASS}@{settings.DB_IP}:" \
                         f"{settings.DB_PORT}/{settings.DB_NAME}_test"

engine = create_engine(SQLACHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
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


@pytest.fixture
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


@pytest.fixture
def test_user_2(client):
    user_data = {
        "email": "use2r@email.com",
        "password": "123"
    }

    res = client.post("/users", json=user_data)

    assert res.status_code == status.HTTP_201_CREATED

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorised_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session, test_user_2):
    posts_data = [
        {
            "title": "t1",
            "content": "c1",
            "owner_id": test_user["id"]
        },
        {
            "title": "t2",
            "content": "c2",
            "owner_id": test_user["id"]
        },
        {
            "title": "t3",
            "content": "c3",
            "owner_id": test_user["id"]
        },
        {
            "title": "t4",
            "content": "c4",
            "owner_id": test_user_2["id"]
        }
    ]

    def create_post_model(post):
        return models.Post(**post)

    posts = list(map(create_post_model, posts_data))
    session.add_all(posts)
    session.commit()
    return session.query(models.Post).all()

    session.add_all([models.User()])
