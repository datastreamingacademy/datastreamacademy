# backend/app/migration.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .models import Base, Course, Lesson, Resource, lesson_prerequisites
import json
from datetime import datetime

# Use the same database URL as in database.py
SQLALCHEMY_DATABASE_URL = "sqlite:///./spark_tutorial.db"

def migrate_database():
    # Create engine and session
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        # Step 1: Backup existing data
        print("Backing up existing data...")
        courses = session.query(Course).all()
        lessons = session.query(Lesson).all()
        resources = session.query(Resource).all()

        backup_data = {
            "courses": [
                {
                    "id": c.id,
                    "title": c.title,
                    "description": c.description,
                    "order": c.order,
                    "is_premium": c.is_premium,
                    "category": c.category.value if c.category else None
                } for c in courses
            ],
            "lessons": [
                {
                    "id": l.id,
                    "title": l.title,
                    "description": l.description,
                    "content": l.content,
                    "order": l.order,
                    "difficulty": l.difficulty.value if l.difficulty else None,
                    "lesson_type": l.lesson_type.value if l.lesson_type else None,
                    "estimated_time": l.estimated_time,
                    "learning_objectives": l.learning_objectives,
                    "is_premium": l.is_premium,
                    "course_id": l.course_id
                } for l in lessons
            ],
            "resources": [
                {
                    "id": r.id,
                    "title": r.title,
                    "type": r.type,
                    "content": r.content,
                    "lesson_id": r.lesson_id
                } for r in resources
            ]
        }

        with open('database_backup.json', 'w') as f:
            json.dump(backup_data, f, indent=2)

        # Step 2: Run any necessary migrations
        current_time = datetime.utcnow()
        
        print("Database migration completed successfully!")

    except Exception as e:
        print(f"Error during migration: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    print("Starting database migration...")
    migrate_database()
    print("Migration complete!")