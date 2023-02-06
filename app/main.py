from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from app.schemas import PostCreate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World!!!"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/{id_}")
def get_post(id_: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id_).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post With Id {id_} Not Found!")

    return {"post": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    post = models.Post(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"data": post}


@app.delete("/posts/{id_}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id_: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id_)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id_} Doesn't Exist!")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id_}")
def update_post(id_: int, updated_post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id_)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id_} Doesn't Exist!")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return {"data": post_query.first()}
