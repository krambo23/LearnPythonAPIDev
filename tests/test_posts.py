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
