from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from ..models.user import User, UserCreate, UserPreferences, Token
from ..utils.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)
from ..core.config import get_settings
from ..db.session import get_db
from ..db.models import User as UserModel, UserPreferences as UserPreferencesModel

router = APIRouter(prefix="/users", tags=["users"])
settings = get_settings()

@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create user preferences
    db_preferences = UserPreferencesModel(user_id=db_user.id)
    db.add(db_preferences)
    db.commit()
    
    return db_user

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    # Get user from database
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.get("/me/preferences", response_model=UserPreferences)
async def get_user_preferences(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user preferences"""
    preferences = db.query(UserPreferencesModel).filter(
        UserPreferencesModel.user_id == current_user.id
    ).first()
    return preferences

@router.put("/me/preferences", response_model=UserPreferences)
async def update_user_preferences(
    preferences: UserPreferences,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user preferences"""
    db_preferences = db.query(UserPreferencesModel).filter(
        UserPreferencesModel.user_id == current_user.id
    ).first()
    
    for key, value in preferences.dict(exclude_unset=True).items():
        setattr(db_preferences, key, value)
    
    db.commit()
    db.refresh(db_preferences)
    return db_preferences

@router.post("/me/watchlist/{movie_id}")
async def add_to_watchlist(
    movie_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a movie to user's watchlist"""
    preferences = db.query(UserPreferencesModel).filter(
        UserPreferencesModel.user_id == current_user.id
    ).first()
    
    if movie_id in preferences.watchlist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie already in watchlist"
        )
    
    preferences.watchlist.append(movie_id)
    db.commit()
    return {"message": "Movie added to watchlist"}

@router.delete("/me/watchlist/{movie_id}")
async def remove_from_watchlist(
    movie_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a movie from user's watchlist"""
    preferences = db.query(UserPreferencesModel).filter(
        UserPreferencesModel.user_id == current_user.id
    ).first()
    
    if movie_id not in preferences.watchlist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie not in watchlist"
        )
    
    preferences.watchlist.remove(movie_id)
    db.commit()
    return {"message": "Movie removed from watchlist"} 