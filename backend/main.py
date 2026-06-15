from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.database import Base, engine, get_db
from backend.helper import get_user_id
from backend.services import RelationshipService
from backend.settings import get_settings


settings = get_settings()
app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def startup() -> None:
    if settings.auto_create_tables:
        Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/db-test")
def db_test(session: Session = Depends(get_db)):
    value = session.execute(text("select 1")).scalar_one()
    return {"data": value}

@app.post("/like/{to_user_id}")
def like_user(to_user_id: str, current_user=Depends(get_user_id), session: Session = Depends(get_db)):
    try:
        service = RelationshipService(session)
        result = service.like_user(current_user, to_user_id)
        session.commit()
        return {"status": result}
    except HTTPException:
        session.rollback()
        raise
    except Exception:
        session.rollback()
        raise
    
@app.post("/friend/{to_user_id}")
def friend_user(to_user_id: str, current_user=Depends(get_user_id), session: Session = Depends(get_db)):
    try:
        service = RelationshipService(session)
        result = service.friend_user(current_user, to_user_id)
        session.commit()
        return {"status": result}
    except HTTPException:
        session.rollback()
        raise
    except Exception:
        session.rollback()
        raise
    