from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Access environment variables
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

def connect_to_database():
    # Construct the database URL
    db_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    try:
        # Create an engine to manage connections
        engine = create_engine(db_url)
        
        # Test the connection
        engine.connect()
        
        return engine
    except SQLAlchemyError as e:
        print("Error connecting to PostgreSQL database:", e)
        return None
