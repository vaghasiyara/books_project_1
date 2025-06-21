from sqlmodel import create_engine, SQLModel
from models.database import Chapter
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bookpub.db")
engine = create_engine(DATABASE_URL, echo=True)

async def init_db():
    SQLModel.metadata.create_all(engine)
