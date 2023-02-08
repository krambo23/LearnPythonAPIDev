from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
import app.oauth2 as oauth2
from typing import List


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/{id_}", response_model=schemas.Post)
def get_post(id_: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id_).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post With Id {id_} Not Found!")

    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post = models.Post(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{id_}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id_: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id_)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id_} Doesn't Exist!")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id_}", response_model=schemas.Post)
def update_post(id_: int, updated_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id_)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id_} Doesn't Exist!")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
