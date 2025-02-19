# backend/app/routes/lessons.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models import Lesson, User
from ..auth.dependencies import get_current_user, get_optional_current_user
from .. import schemas

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.get("/{lesson_id}")
async def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get lesson by ID. Premium lessons require authentication.
    """
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Check premium access
    if lesson.is_premium and (not current_user or not current_user.is_premium):
        raise HTTPException(
            status_code=403,
            detail="This lesson requires premium access"
        )
    
    return lesson

@router.get("/{lesson_id}/progress")
async def get_lesson_progress(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Required auth
):
    """
    Get user's progress for a specific lesson. Requires authentication.
    """
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    progress = db.query(UserProgress).filter(
        UserProgress.lesson_id == lesson_id,
        UserProgress.user_id == current_user.id
    ).first()

    return progress or {"is_completed": False, "completed_at": None}