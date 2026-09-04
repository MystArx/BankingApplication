from database.database_connection import engine
from models.models import Base

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Successfully created tables")
    except Exception as e:
        print(f"Error creating tables: {e}")
