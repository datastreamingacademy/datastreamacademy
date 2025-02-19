# backend/app/inspect_db.py
from sqlalchemy import inspect, text
from app.database import engine, SessionLocal
from app.models import Course, Lesson, Resource

def inspect_database():
    """Inspect the database contents and structure"""
    db = SessionLocal()
    try:
        # Get database inspector
        inspector = inspect(engine)
        
        # Print table structures
        print("\n=== Database Structure ===")
        for table_name in inspector.get_table_names():
            print(f"\nTable: {table_name}")
            for column in inspector.get_columns(table_name):
                print(f"  - {column['name']}: {column['type']}")
        
        # Count records
        print("\n=== Record Counts ===")
        course_count = db.query(Course).count()
        lesson_count = db.query(Lesson).count()
        resource_count = db.query(Resource).count()
        
        print(f"Courses: {course_count}")
        print(f"Lessons: {lesson_count}")
        print(f"Resources: {resource_count}")
        
        # Print course details if any exist
        if course_count > 0:
            print("\n=== Course Details ===")
            courses = db.query(Course).all()
            for course in courses:
                print(f"\nCourse ID: {course.id}")
                print(f"Title: {course.title}")
                print(f"Description: {course.description}")
                print(f"Order: {course.order}")
                print(f"Is Premium: {course.is_premium}")
                
                # Try to access timestamps
                try:
                    print(f"Created At: {course.created_at}")
                    print(f"Updated At: {course.updated_at}")
                except Exception as e:
                    print(f"Error accessing timestamps: {str(e)}")
        
    except Exception as e:
        print(f"Error during inspection: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting database inspection...")
    inspect_database()
    print("\nInspection complete!")