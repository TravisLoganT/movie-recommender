from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserPreferences(BaseModel):
    favorite_genres: List[int] = Field(default_factory=list)
    favorite_movies: List[int] = Field(default_factory=list)
    watchlist: List[int] = Field(default_factory=list)
    language_preference: str = "en-US"
    adult_content: bool = False

class UserInDB(UserBase):
    id: int
    hashed_password: str
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

class User(UserBase):
    id: int
    preferences: UserPreferences
    created_at: datetime
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None 