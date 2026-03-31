from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional

from backend.schema.models import UserIn, UserOut, PostCreate, PostShow
from backend.db.session import get_db
from backend.auth.hash import hash_password, verify_password
from backend.auth.auth import create_access_token, decode_token
from backend.auth.gate import current_user
from backend.schema import db_models

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://fast-post-lovat.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/Register", response_model=UserOut)
def register_user(user: UserIn, db: Session = Depends(get_db)):
    existing_user = (
        db.query(db_models.User)
        .filter(db_models.User.email == user.email)
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    username_exists = (
        db.query(db_models.User)
        .filter(db_models.User.username == user.username)
        .first()
    )
    if username_exists:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = db_models.User(
        name=user.name,
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
def login_user(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = (
        db.query(db_models.User)
        .filter(db_models.User.username == form_data.username)
        .first()
    )
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    access_token = create_access_token(user_id=user.user_id, role="user")
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/post")
def create_post(post: PostCreate, db: Session = Depends(get_db), current: dict = Depends(current_user)):
    new_post = db_models.Post(
        user_id=current["user"].user_id,
        content_type=post.content_type,
        title=post.title,
        post=post.post,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"Message": "Post Created"}


# Current user's posts
@app.get("/post", response_model=list[PostShow])
def show_my_posts(username: str, db: Session = Depends(get_db), current: dict = Depends(current_user)):
    posts = (
        db.query(db_models.Post)
        .filter(db_models.Post.user_id == current["user"].user_id)
        .all()
    )
    return [
        {
            "post_id": p.post_id,
            "username": username,
            "content_type": p.content_type,
            "title": p.title,
            "post": p.post,
            "created_at": p.created_at,
        }
        for p in posts
    ]



@app.get("/posts", response_model=list[PostShow])
def show_all_posts(content_type: Optional[str] = None, db: Session = Depends(get_db), current: dict = Depends(current_user)):
    query = db.query(db_models.Post).join(db_models.User)
    if content_type and content_type.lower() != "all":
        query = query.filter(db_models.Post.content_type == content_type)
    posts = query.all()
    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found")
    return [
        {
            "post_id": p.post_id,
            "username": p.user.username,
            "content_type": p.content_type,
            "title": p.title,
            "post": p.post,
            "created_at": p.created_at,
        }
        for p in posts
    ]


@app.put("/post/{post_id}")
def update_post(post_id: int, username: str, post: PostCreate, db: Session = Depends(get_db), current: dict = Depends(current_user)):
    existing_post = (
        db.query(db_models.Post)
        .filter(db_models.Post.post_id == post_id)
        .first()
    )
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if existing_post.user_id != current["user"].user_id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")

    existing_post.content_type = post.content_type
    existing_post.title = post.title
    existing_post.post = post.post
    db.commit()
    db.refresh(existing_post)
    return {"Message": "Post Updated"}


@app.delete("/post")
def delete_all_posts(username: str, db: Session = Depends(get_db), current: dict = Depends(current_user)):
    db.query(db_models.Post).filter(db_models.Post.user_id == current["user"].user_id).delete()
    db.commit()
    return {"Message": "Posts Deleted"}


@app.delete("/post/{post_id}")
def delete_post(post_id: int, username: str, db: Session = Depends(get_db), current: dict = Depends(current_user)):
    post = (
        db.query(db_models.Post)
        .filter(db_models.Post.post_id == post_id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current["user"].user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    db.delete(post)
    db.commit()
    return {"Message": "Post Deleted"}
