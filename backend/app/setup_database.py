# backend/app/setup_database.py
import os
import sys
from .migration import migrate_database
from .seed import seed_data
from .models import Base
from .database import engine

def setup_database():
    try:
        # Step 1: Create backup of existing database if it exists
        if os.path.exists("./spark_tutorial.db"):
            print("Creating backup of existing database...")
            backup_filename = "spark_tutorial.db.backup"
            counter = 1
            while os.path.exists(backup_filename):
                backup_filename = f"spark_tutorial.db.backup.{counter}"
                counter += 1
            os.rename("spark_tutorial.db", backup_filename)
            print(f"Backup created as {backup_filename}")

        # Step 2: Create new database tables
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")

        # Step 3: Run migrations
        print("Running database migrations...")
        migrate_database()
        print("Migrations completed successfully!")

        # Step 4: Seed initial data
        print("Seeding initial data...")
        seed_data()
        print("Data seeding completed successfully!")

        print("Database setup completed successfully!")
        return True

    except Exception as e:
        print(f"Error during database setup: {str(e)}")
        
        # Attempt to restore backup if it exists
        if 'backup_filename' in locals():
            print(f"Attempting to restore from backup {backup_filename}...")
            try:
                if os.path.exists("./spark_tutorial.db"):
                    os.remove("./spark_tutorial.db")
                os.rename(backup_filename, "spark_tutorial.db")
                print("Backup restored successfully!")
            except Exception as restore_error:
                print(f"Error restoring backup: {str(restore_error)}")
                print(f"Backup file is still available at: {backup_filename}")
        
        return False

if __name__ == "__main__":
    print("Starting database setup process...")
    success = setup_database()
    sys.exit(0 if success else 1)