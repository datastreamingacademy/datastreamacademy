# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import traceback
from datetime import datetime

# Import models, schemas, and dependencies
from . import models, schemas
from .database import engine, get_db
from .core.config import settings
from .auth.oauth_routes import router as oauth_router
from .auth.validation import router as validation_router
from .auth.dependencies import get_current_user, get_optional_current_user
from .utils.progress import ProgressTracker

# Import necessary types
from .models import User, Lesson, Course

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Spark Tutorial API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(oauth_router)
app.include_router(validation_router)

# Add a health check endpoint
@app.get("/")
async def health_check():
    return {
        "status": "healthy",
        "message": "Backend server is running"
    }

# Course endpoints
@app.get("/courses")
def get_courses(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    try:
        print("\n=== Fetching Courses ===")
        print("Querying database...")
        
        # Get courses with explicit columns
        courses = db.query(
            models.Course.id,
            models.Course.title,
            models.Course.description,
            models.Course.order,
            models.Course.is_premium
        ).order_by(models.Course.order).offset(skip).limit(limit).all()
        
        print(f"Found {len(courses) if courses else 0} courses")
        
        # Convert to list of dictionaries
        courses_data = [
            {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "order": course.order,
                "is_premium": course.is_premium,
            }
            for course in courses
        ]
        
        print("Courses data:", courses_data)
        
        return {"courses": courses_data}
        
    except Exception as e:
        print("\n=== Error in /courses endpoint ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nTraceback:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Internal server error",
                "error_type": type(e).__name__,
                "error_details": str(e)
            }
        )

@app.get("/courses/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    try:
        print(f"\nFetching course with ID: {course_id}")
        course = db.query(models.Course)\
            .filter(models.Course.id == course_id)\
            .first()
            
        if course is None:
            print(f"Course {course_id} not found")
            raise HTTPException(status_code=404, detail="Course not found")
            
        print(f"Found course: {course.title}")
        
        # Convert to dict for consistency
        course_data = {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "order": course.order,
            "is_premium": course.is_premium
        }
        
        return course_data
        
    except Exception as e:
        print(f"Error fetching course {course_id}: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

# Lesson endpoints
@app.get("/lessons", response_model=List[schemas.LessonRead])
def get_lessons(
    skip: int = 0, 
    limit: int = 100,
    course_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        print("\n=== Fetching Lessons ===")
        query = db.query(models.Lesson)
        
        # Optional filtering by course
        if course_id is not None:
            query = query.filter(models.Lesson.course_id == course_id)
        
        # Order and paginate
        lessons = query\
            .order_by(models.Lesson.order)\
            .offset(skip)\
            .limit(limit)\
            .all()
        
        print(f"Found {len(lessons)} lessons")
        
        return lessons
        
    except Exception as e:
        print(f"Error fetching lessons: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/lessons/{lesson_id}")
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    try:
        print(f"\nFetching lesson with ID: {lesson_id}")
        lesson = db.query(models.Lesson)\
            .filter(models.Lesson.id == lesson_id)\
            .first()
            
        if lesson is None:
            print(f"Lesson {lesson_id} not found")
            raise HTTPException(status_code=404, detail="Lesson not found")
        
        print(f"Found lesson: {lesson.title}")
        
        # Convert to dict for consistent serialization
        lesson_data = {
            "id": lesson.id,
            "title": lesson.title,
            "description": lesson.description,
            "content": lesson.content,
            "content_sections": lesson.content_sections or [],
            "code_samples": lesson.code_samples or [],
            "key_points": lesson.key_points,
            "order": lesson.order,
            "difficulty": lesson.difficulty.value if lesson.difficulty else "beginner",
            "lesson_type": lesson.lesson_type.value if lesson.lesson_type else "theory",
            "estimated_time": lesson.estimated_time,
            "learning_objectives": lesson.learning_objectives,
            "is_premium": lesson.is_premium,
            "course_id": lesson.course_id
        }
        
        return lesson_data
        
    except Exception as e:
        print(f"Error fetching lesson {lesson_id}: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/lessons/{lesson_id}/resources")
def get_lesson_resources(lesson_id: int, db: Session = Depends(get_db)):
    try:
        print(f"\nFetching resources for lesson ID: {lesson_id}")
        resources = db.query(models.Resource)\
            .filter(models.Resource.lesson_id == lesson_id)\
            .all()
            
        resources_data = [
            {
                "id": resource.id,
                "title": resource.title,
                "type": resource.type,
                "content": resource.content,
                "description": resource.description if hasattr(resource, 'description') else None
            }
            for resource in resources
        ]
        
        print(f"Found {len(resources_data)} resources")
        return {"resources": resources_data}
        
    except Exception as e:
        print(f"Error fetching resources for lesson {lesson_id}: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/lessons/{lesson_id}/navigation")
def get_lesson_navigation(lesson_id: int, db: Session = Depends(get_db)):
    try:
        print(f"\nFetching navigation for lesson ID: {lesson_id}")
        current_lesson = db.query(models.Lesson)\
            .filter(models.Lesson.id == lesson_id)\
            .first()
            
        if not current_lesson:
            print(f"Lesson {lesson_id} not found")
            raise HTTPException(status_code=404, detail="Lesson not found")
        
        # Find previous lesson in same course
        prev_lesson = db.query(models.Lesson)\
            .filter(
                models.Lesson.course_id == current_lesson.course_id,
                models.Lesson.order < current_lesson.order
            )\
            .order_by(models.Lesson.order.desc())\
            .first()
        
        # Find next lesson in same course
        next_lesson = db.query(models.Lesson)\
            .filter(
                models.Lesson.course_id == current_lesson.course_id,
                models.Lesson.order > current_lesson.order
            )\
            .order_by(models.Lesson.order.asc())\
            .first()
        
        navigation_data = {
            "previous": {
                "id": prev_lesson.id,
                "title": prev_lesson.title
            } if prev_lesson else None,
            "next": {
                "id": next_lesson.id,
                "title": next_lesson.title
            } if next_lesson else None
        }
        
        print("Navigation data:", navigation_data)
        return navigation_data
        
    except Exception as e:
        print(f"Error fetching lesson navigation for lesson {lesson_id}: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/courses/{course_id}/lessons")
def get_course_lessons(course_id: int, db: Session = Depends(get_db)):
    try:
        print(f"\nFetching lessons for course ID: {course_id}")
        lessons = db.query(models.Lesson)\
            .filter(models.Lesson.course_id == course_id)\
            .order_by(models.Lesson.order)\
            .all()
            
        print(f"Found {len(lessons)} lessons")
        
        # Convert to list of dicts
        lessons_data = [
            {
                "id": lesson.id,
                "title": lesson.title,
                "description": lesson.description,
                "content": lesson.content,
                "order": lesson.order,
                "difficulty": lesson.difficulty.value if lesson.difficulty else "beginner",
                "lesson_type": lesson.lesson_type.value if lesson.lesson_type else "theory",
                "estimated_time": lesson.estimated_time,
                "learning_objectives": lesson.learning_objectives,
                "is_premium": lesson.is_premium
            }
            for lesson in lessons
        ]
        
        return {"lessons": lessons_data}
        
    except Exception as e:
        print(f"Error fetching lessons for course {course_id}: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

# Progress tracking endpoints
@app.post("/lessons/{lesson_id}/progress", response_model=schemas.UserProgressRead)
def update_lesson_progress(
    lesson_id: int, 
    is_completed: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update progress for a specific lesson for the authenticated user.
    """
    try:
        # Check if lesson exists
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        
        # Use ProgressTracker to update lesson progress
        progress_tracker = ProgressTracker(db)
        progress = progress_tracker.update_lesson_progress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            is_completed=is_completed
        )
        
        return progress
    
    except Exception as e:
        print(f"Error updating lesson progress: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not update lesson progress")

@app.get("/lessons/{lesson_id}/progress", response_model=Optional[schemas.UserProgressRead])
def get_lesson_progress(
    lesson_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve progress for a specific lesson for the authenticated user.
    """
    try:
        progress_tracker = ProgressTracker(db)
        progress = progress_tracker.get_user_lesson_progress(
            user_id=current_user.id,
            lesson_id=lesson_id
        )
        
        return progress
    
    except Exception as e:
        print(f"Error fetching lesson progress: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not retrieve lesson progress")

@app.get("/courses/{course_id}/progress", response_model=dict)
def get_course_progress(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get overall progress for a specific course.
    """
    try:
        progress_tracker = ProgressTracker(db)
        course_progress = progress_tracker.get_course_progress(
            user_id=current_user.id,
            course_id=course_id
        )
        
        return course_progress
    
    except Exception as e:
        print(f"Error fetching course progress: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not retrieve course progress")

@app.get("/progress", response_model=List[dict])
def get_all_courses_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get progress for all courses a user has started.
    """
    try:
        progress_tracker = ProgressTracker(db)
        all_courses_progress = progress_tracker.get_all_courses_progress(
            user_id=current_user.id
        )
        
        return all_courses_progress
    
    except Exception as e:
        print(f"Error fetching all courses progress: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not retrieve courses progress")