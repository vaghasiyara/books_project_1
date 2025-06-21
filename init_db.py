from sqlmodel import SQLModel, create_engine
from models.database import Chapter
import os

print("Initializing database...")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bookpub.db")
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    print(f"Database created at: {os.path.abspath('bookpub.db')}")

if __name__ == "__main__":
    create_db_and_tables()
