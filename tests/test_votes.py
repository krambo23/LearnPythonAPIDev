import pytest
from app import models
from fastapi import status


def test_vote_on_post(authorised_client, test_posts):
    res = authorised_client.post("/vote", json={"post_id": test_posts[3].id, "direction": 1})
    assert res.status_code == status.HTTP_201_CREATED


def test_double_vote_post(authorised_client, test_posts, test_vote):
    res = authorised_client.post("/vote", json={"post_id": test_posts[3].id, "direction": 1})
    assert res.status_code == status.HTTP_409_CONFLICT


def test_delete_vote(authorised_client, test_posts, test_vote):
    res = authorised_client.post("/vote", json={"post_id": test_posts[3].id, "direction": 0})
    assert res.status_code == status.HTTP_201_CREATED


def test_delete_vote_non_exist(authorised_client, test_posts):
    res = authorised_client.post("/vote", json={"post_id": test_posts[3].id, "direction": 0})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_vote_post_non_exist(authorised_client, test_posts):
    res = authorised_client.post("/vote", json={"post_id": "696969", "direction": 1})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_vote_unauthorised_user(client, test_posts):
    res = client.post("/vote", json={"post_id": test_posts[3].id, "direction": 1})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
