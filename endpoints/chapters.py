from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import engine
from models.database import Chapter
from auth import oauth2_scheme, get_current_user
from datetime import datetime

router = APIRouter(prefix="/chapters", tags=["chapters"])

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/", dependencies=[Depends(get_current_user)])
async def create_chapter(chapter: Chapter, session: Session = Depends(get_session)):
    session.add(chapter)
    session.commit()
    session.refresh(chapter)
    return chapter

@router.get("/{chapter_id}/versions")
async def get_chapter_versions(chapter_id: int, session: Session = Depends(get_session)):
    chapter = session.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    versions = session.exec(
        select(Chapter).where(Chapter.title == chapter.title)
    ).all()
    return versions
