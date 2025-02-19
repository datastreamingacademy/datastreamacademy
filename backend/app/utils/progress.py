# backend/app/utils/progress.py
"""
Progress tracking utilities for the Spark Tutorial platform.
This module provides functionality for tracking and managing user progress
through courses and lessons.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Optional

from ..models import User, Lesson, Course, UserProgress
from ..schemas import UserProgressRead

class ProgressTracker:
    """
    Utility class for managing user progress tracking
    """
    def __init__(self, db: Session):
        self.db = db

    def get_user_lesson_progress(
        self, 
        user_id: int, 
        lesson_id: int
    ) -> Optional[UserProgress]:
        """
        Get a user's progress for a specific lesson
        """
        return self.db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.lesson_id == lesson_id
        ).first()

    def get_course_progress(
        self, 
        user_id: int, 
        course_id: int
    ) -> Dict:
        """
        Calculate user's progress in a specific course
        """
        # Get total lessons in course
        total_lessons = self.db.query(func.count(Lesson.id)).filter(
            Lesson.course_id == course_id
        ).scalar()

        # Get completed lessons
        completed_lessons = self.db.query(func.count(UserProgress.id)).filter(
            UserProgress.user_id == user_id,
            UserProgress.is_completed == True,
            Lesson.course_id == course_id
        ).join(Lesson).scalar()

        # Get last accessed lesson
        last_accessed = self.db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            Lesson.course_id == course_id
        ).join(Lesson).order_by(
            UserProgress.updated_at.desc()
        ).first()

        return {
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "completion_percentage": (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0,
            "last_accessed_lesson_id": last_accessed.lesson_id if last_accessed else None,
            "last_accessed_at": last_accessed.updated_at if last_accessed else None
        }

    def get_all_courses_progress(
        self, 
        user_id: int
    ) -> List[Dict]:
        """
        Get progress for all courses a user has started
        """
        courses = self.db.query(Course).all()
        return [
            {
                "course_id": course.id,
                "course_title": course.title,
                **self.get_course_progress(user_id, course.id)
            }
            for course in courses
        ]

    def update_lesson_progress(
        self,
        user_id: int,
        lesson_id: int,
        is_completed: bool = True
    ) -> UserProgress:
        """
        Update or create progress record for a lesson
        """
        progress = self.get_user_lesson_progress(user_id, lesson_id)
        
        if not progress:
            progress = UserProgress(
                user_id=user_id,
                lesson_id=lesson_id,
                is_completed=is_completed,
                completed_at=datetime.utcnow() if is_completed else None
            )
            self.db.add(progress)
        else:
            progress.is_completed = is_completed
            progress.completed_at = datetime.utcnow() if is_completed else None
            progress.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(progress)
        return progress

    def get_next_lesson(
        self, 
        user_id: int, 
        course_id: int
    ) -> Optional[Lesson]:
        """
        Get the next uncompleted lesson in a course
        """
        # Get all completed lesson IDs for the user in this course
        completed_lesson_ids = self.db.query(UserProgress.lesson_id).filter(
            UserProgress.user_id == user_id,
            UserProgress.is_completed == True,
            Lesson.course_id == course_id
        ).join(Lesson).all()
        
        completed_ids = [lid for (lid,) in completed_lesson_ids]

        # Find the first uncompleted lesson
        next_lesson = self.db.query(Lesson).filter(
            Lesson.course_id == course_id,
            ~Lesson.id.in_(completed_ids)
        ).order_by(Lesson.order).first()

        return next_lesson