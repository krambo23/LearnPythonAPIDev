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

