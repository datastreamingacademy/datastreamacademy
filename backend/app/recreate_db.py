# backend/app/recreate_db.py
from app.database import engine
from app.models import Base
from app.seed import seed_data

def recreate_database():
    """Recreate the database from scratch with the updated schema"""
    try:
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("Creating all tables with new schema...")
        Base.metadata.create_all(bind=engine)
        print("Seeding database...")
        seed_data()
        print("Database recreation completed successfully!")
        return True
    except Exception as e:
        print(f"Error recreating database: {str(e)}")
        return False

def verify_database():
    """Verify database schema and contents"""
    from sqlalchemy import inspect
    
    inspector = inspect(engine)
    
    print("\nVerifying database schema:")
    
    # Check tables
    tables = inspector.get_table_names()
    print("\nFound tables:", tables)
    
    # Check columns for each table
    for table in tables:
        columns = inspector.get_columns(table)
        print(f"\nColumns in {table}:")
        for column in columns:
            print(f"  - {column['name']}: {column['type']}")
    
    print("\nSchema verification completed!")

if __name__ == "__main__":
    print("Starting database recreation...")
    if recreate_database():
        verify_database()
    print("Done!")