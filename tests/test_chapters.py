import pytest
from models.database import Chapter

def test_create_chapter(test_db, test_client):
    test_chapter = {
        "title": "Test Chapter",
        "content": "Test content",
        "version": 1
    }
    
    response = test_client.post("/chapters/", json=test_chapter)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Chapter"
