from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey, Boolean, func
from datetime import datetime


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    user_id:Mapped[int] = mapped_column(primary_key = True, autoincrement = True, index = True)
    name: Mapped[str] = mapped_column(String)
    username:Mapped[str] = mapped_column(String)
    email:Mapped[str] = mapped_column(String, unique = True)
    hashed_password:Mapped[str] = mapped_column(String, nullable = False)

    posts = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"
    )

class Post(Base):
    __tablename__ = "posts"

    post_id:Mapped[int] = mapped_column(primary_key = True, autoincrement = True, index = True)
    user_id = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )
    content_type:Mapped[str] = mapped_column(String(20))
    title:Mapped[str] = mapped_column(String(20))
    post:Mapped[str] = mapped_column(String(500))
    created_at:Mapped[datetime] = mapped_column(DateTime, nullable = False, server_default=func.now())
    #When this row is inserted, let the database server fill this column using its own NOW() function.

    user = relationship(
        "User",
        back_populates="posts",
    )