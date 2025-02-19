# backend/app/auth/validation.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from jose import JWTError, jwt

from ..database import get_db
from ..models import User
from ..core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

async def get_current_user(
    token: str,
    db: Session = Depends(get_db)
) -> Optional[User]:
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=["HS256"]
        )
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/validate")
async def validate_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Validate JWT token and return user information"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "picture": current_user.picture
    }