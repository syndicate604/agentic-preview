import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from agentic_platform.agentic_platform.models import Base, Project
from agentic_platform.agentic_platform.database import DATABASE_URL as SQLALCHEMY_DATABASE_URL

# Create a new engine instance
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def update_database():
    # Create a new session
    db = SessionLocal()

    try:
        from sqlalchemy import text

        # Rename the existing table
        db.execute(text("ALTER TABLE projects RENAME TO old_projects"))

        # Create the new table with the updated schema
        Base.metadata.create_all(bind=engine)

        # Copy data from the old table to the new one
        db.execute(text("""
            INSERT INTO projects (id, name, user_id, created_at, last_updated, total_cost)
            SELECT id, name, user_id, created_at, last_updated, total_cost
            FROM old_projects
        """))

        # Drop the old table
        db.execute(text("DROP TABLE old_projects"))

        # Commit the transaction
        db.commit()
        print("Database updated successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_database()
