from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    preferences = relationship("UserPreferences", back_populates="user", uselist=False)

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    favorite_genres = Column(JSON, default=list)
    favorite_movies = Column(JSON, default=list)
    watchlist = Column(JSON, default=list)
    language_preference = Column(String, default="en-US")
    adult_content = Column(Boolean, default=False)

    user = relationship("User", back_populates="preferences") 