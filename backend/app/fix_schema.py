# backend/app/fix_schema.py
from sqlalchemy import text
from app.database import engine, SessionLocal

def fix_schema():
    """Add all missing columns to the database tables"""
    db = SessionLocal()
    try:
        print("Adding missing columns to lessons table...")
        
        # New columns for lessons table
        lesson_columns = [
            ("summary", "TEXT"),
            ("content_sections", "TEXT"),
            ("code_samples", "TEXT"),
            ("key_points", "TEXT"),
            ("skill_level_required", "TEXT"),
            ("created_at", "TIMESTAMP"),
            ("updated_at", "TIMESTAMP")
        ]
        
        # Add columns one by one
        for column_name, column_type in lesson_columns:
            try:
                db.execute(text(f"ALTER TABLE lessons ADD COLUMN {column_name} {column_type}"))
                print(f"Added column {column_name} to lessons table")
            except Exception as e:
                print(f"Note: Could not add column {column_name}: {str(e)}")
        
        print("\nAdding timestamp columns to other tables...")
        
        # Add timestamps to courses and resources
        for table in ['courses', 'resources']:
            for column in ['created_at', 'updated_at']:
                try:
                    db.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} TIMESTAMP"))
                    print(f"Added column {column} to {table} table")
                except Exception as e:
                    print(f"Note: Could not add column {column} to {table}: {str(e)}")
        
        db.commit()
        print("\nSchema update completed!")
        return True
        
    except Exception as e:
        print(f"Error during schema update: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

def verify_schema():
    """Verify that all required columns exist"""
    db = SessionLocal()
    try:
        print("\nVerifying schema...")
        
        # Test query to check all columns
        test_queries = [
            "SELECT title, description, summary, content_sections, code_samples, key_points, created_at, updated_at FROM lessons LIMIT 1",
            "SELECT title, description, created_at, updated_at FROM courses LIMIT 1",
            "SELECT title, content, created_at, updated_at FROM resources LIMIT 1"
        ]
        
        for query in test_queries:
            try:
                db.execute(text(query))
                print(f"✓ Query passed: {query}")
            except Exception as e:
                print(f"✗ Query failed: {query}")
                print(f"Error: {str(e)}")
                return False
        
        print("\nSchema verification completed!")
        return True
        
    except Exception as e:
        print(f"Error during schema verification: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting schema fix...")
    if fix_schema():
        verify_schema()
    print("Done!")