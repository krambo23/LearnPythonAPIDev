from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
    # phone_number = Column(String)


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))

    owner_id = Column(Integer, ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE"),
                     primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey(f"{Post.__tablename__}.id", ondelete="CASCADE"),
                     primary_key=True, nullable=False)
