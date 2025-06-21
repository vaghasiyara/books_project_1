from celery import Celery
from sqlmodel import Session
from models.database import Chapter
from database import engine

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def publish_chapter(chapter_id: int):
    with Session(engine) as session:
        chapter = session.get(Chapter, chapter_id)
        if chapter:
            chapter.is_published = True
            session.add(chapter)
            session.commit()
