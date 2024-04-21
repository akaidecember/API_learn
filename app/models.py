from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    owner = relationship('User')

class User(Base):
    __tablename__ = 'users'

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Vote(Base):
    __tablename__ = 'votes'

    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)