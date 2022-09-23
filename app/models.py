from enum import unique
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null, text
from .database import Base

class Post (Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = 'True', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text("NOW()"))
    # user since it is referencing the table
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False)

    # User since it is referencing the class
    # Uses the foerign key relationship to fetch user
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text("NOW()"))


class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key = True, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key = True, nullable = False)