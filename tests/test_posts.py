import pytest
from fastapi import status
from typing import List
from app import schemas


def test_get_all_posts(authorised_client, test_posts):
    res = authorised_client.get("/posts")

    def validate(post):
        return schemas.PostOut(**post)

    posts = list(map(validate, res.json()))

    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == len(test_posts)


def test_get_one_post(authorised_client, test_posts):
    res = authorised_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert res.status_code == status.HTTP_200_OK
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content


def test_unauthorised_user_get_all_posts(client, test_posts):
    res = client.get("/posts")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorised_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_non_existent_post(authorised_client, test_posts):
    res = authorised_client.get("/posts/696969")
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("title, content, published", [
    ("Ttl1", "CNT1", True),
    ("Ttl2", "CNT2", False),
    ("Ttl3", "CNT3", True),
    ("Ttl4", "CNT4", True),
])
def test_create_post(authorised_client, test_user, test_posts, title, content, published):
    res = authorised_client.post("/posts", json={
        "title": title,
        "content": content,
        "published": published
    })

    post = schemas.Post(**res.json())

    assert res.status_code == status.HTTP_201_CREATED
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.owner_id == test_user["id"]


@pytest.mark.parametrize("title, content", [
    ("Ttl1", "CNT1"),
    ("Ttl2", "CNT2"),
    ("Ttl3", "CNT3"),
    ("Ttl4", "CNT4"),
])
def test_create_post_default_published_value(authorised_client, test_user, test_posts, title, content):
    res = authorised_client.post("/posts", json={
        "title": title,
        "content": content
    })

    post = schemas.Post(**res.json())

    assert res.status_code == status.HTTP_201_CREATED
    assert post.title == title
    assert post.content == content
    assert post.published is True
    assert post.owner_id == test_user["id"]


def test_unauthorised_user_create_post(client, test_user, test_posts):
    res = client.post("/posts", json={
        "title": "TTL",
        "content": "CNT"
    })
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorised_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_post(authorised_client, test_user, test_posts):
    res = authorised_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_204_NO_CONTENT


def test_delete_non_existent_post(authorised_client, test_user, test_posts):
    res = authorised_client.delete("/posts/696969")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_delete_other_users_post(authorised_client, test_user, test_posts):
    res = authorised_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_update_post(authorised_client, test_user, test_posts):
    data = {
        "title": "UT1",
        "content": "UC1",
        "id": test_posts[0].id
    }
    res = authorised_client.put(f"/posts/{test_posts[0].id}", json=data)
    post = schemas.Post(**res.json())

    assert res.status_code == status.HTTP_200_OK
    assert post.title == data["title"]
    assert post.content == data["content"]


def test_update_other_users_post(authorised_client, test_user, test_user_2, test_posts):
    data = {
        "title": "UT4",
        "content": "UC4",
        "id": test_posts[3].id
    }
    res = authorised_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_unauthorised_user_update_post(client, test_user, test_posts):
    data = {
        "title": "UT4",
        "content": "UC4",
        "id": test_posts[3].id
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_non_existent_post(authorised_client, test_user, test_posts):
    data = {
        "title": "UT4",
        "content": "UC4",
        "id": test_posts[3].id
    }
    res = authorised_client.put("/posts/696969", json=data)
    assert res.status_code == status.HTTP_404_NOT_FOUND

