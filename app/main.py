from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# Temporary - Before Adding DB
my_posts = [
    {
        "title": "P1",
        "content": "C1",
        "id": 1
    },
    {
        "title": "P2",
        "content": "C2",
        "id": 2
    }
]


def find_post_by_id(id_: int):
    for post in my_posts:
        if post["id"] == id_:
            print(post)
            return post


def find_index_of_post(id_: int):
    for index, post in enumerate(my_posts):
        if post["id"] == id_:
            return index


@app.get("/")
def root():
    return {"message": "Hello World!!!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/{id_}")
def get_post(id_: int):
    post = find_post_by_id(id_)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post With Id {id_} Not Found!")

    return {"post": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    from random import randrange
    post = post.dict()
    post["id"] = randrange(0, int(1e7))

    my_posts.append(post)
    return {"data": post}


@app.delete("/posts/{id_}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id_: int):
    index = find_index_of_post(id_)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id_} Doesn't Exist!")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id_}")
def update_post(id_: int, post: Post):
    index = find_index_of_post(id_)
    print(post)
    print(index)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id_} Doesn't Exist!")

    post = post.dict()
    post["id"] = id_
    my_posts[index] = post
    return {"data": post}
