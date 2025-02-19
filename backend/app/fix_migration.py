# backend/app/fix_migration.py
from sqlalchemy import text
from datetime import datetime
from app.database import engine, SessionLocal

def fix_database():
    """Add missing timestamp columns to tables"""
    db = SessionLocal()
    try:
        print("Adding timestamp columns to tables...")
        
        # Add timestamps to courses table
        print("Fixing courses table...")
        try:
            db.execute(text("ALTER TABLE courses ADD COLUMN created_at TIMESTAMP"))
            db.execute(text("ALTER TABLE courses ADD COLUMN updated_at TIMESTAMP"))
        except Exception as e:
            print(f"Note: {str(e)}")  # SQLite might complain if columns exist
            
        # Add timestamps to lessons table
        print("Fixing lessons table...")
        try:
            db.execute(text("ALTER TABLE lessons ADD COLUMN created_at TIMESTAMP"))
            db.execute(text("ALTER TABLE lessons ADD COLUMN updated_at TIMESTAMP"))
        except Exception as e:
            print(f"Note: {str(e)}")
            
        # Add timestamps to resources table
        print("Fixing resources table...")
        try:
            db.execute(text("ALTER TABLE resources ADD COLUMN created_at TIMESTAMP"))
            db.execute(text("ALTER TABLE resources ADD COLUMN updated_at TIMESTAMP"))
        except Exception as e:
            print(f"Note: {str(e)}")
            
        # Update all existing records with current timestamp
        current_time = datetime.utcnow()
        
        print("Updating existing records with timestamps...")
        for table in ['courses', 'lessons', 'resources']:
            db.execute(
                text(f"UPDATE {table} SET created_at = :time, updated_at = :time"),
                {"time": current_time}
            )
        
        db.commit()
        print("Database fix completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during database fix: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting database fix...")
    fix_database()