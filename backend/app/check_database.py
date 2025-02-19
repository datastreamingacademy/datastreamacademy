# backend/app/check_database.py
from sqlalchemy import inspect
from app.database import engine, SessionLocal
from app.models import Base, Course, Lesson, Resource

def check_database():
    """Check database tables and their contents"""
    inspector = inspect(engine)
    session = SessionLocal()
    
    try:
        print("\n=== Database Check ===")
        
        # Check if database file exists
        try:
            engine.connect()
            print("✓ Database connection successful")
        except Exception as e:
            print(f"✗ Database connection failed: {str(e)}")
            return False

        # Check if all tables exist
        existing_tables = inspector.get_table_names()
        required_tables = ['courses', 'lessons', 'resources', 'lesson_prerequisites']
        
        print("\nChecking tables:")
        for table in required_tables:
            if table in existing_tables:
                print(f"✓ Table '{table}' exists")
            else:
                print(f"✗ Table '{table}' is missing")
                return False

        # Check if tables have content
        print("\nChecking table contents:")
        course_count = session.query(Course).count()
        lesson_count = session.query(Lesson).count()
        resource_count = session.query(Resource).count()
        
        print(f"- Courses: {course_count}")
        print(f"- Lessons: {lesson_count}")
        print(f"- Resources: {resource_count}")
        
        if course_count == 0:
            print("✗ No courses found - database needs to be seeded")
            return False
            
        print("\n✓ Database check completed successfully")
        return True

    except Exception as e:
        print(f"\n✗ Error during database check: {str(e)}")
        return False
    finally:
        session.close()

if __name__ == "__main__":
    check_database()