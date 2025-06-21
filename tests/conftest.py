import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, SQLModel, Session
from database import Chapter
from app import app

@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)
