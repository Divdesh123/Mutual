from fastapi import Depends, Header, HTTPException
import jwt
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.settings import get_settings
from backend.services import RelationshipService


def get_user_id(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")

    token = authorization.split(" ", 1)[1].strip()
    settings = get_settings()

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
            options={"verify_aud": settings.jwt_audience is not None},
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    subject = payload.get("sub")
    if not subject:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return subject


def get_relationship_service(session: Session = Depends(get_db)) -> RelationshipService:
    return RelationshipService(session)


def like_user(session: Session, current_user_id: str, target_user_id: str) -> str:
    service = RelationshipService(session)
    return service.like_user(current_user_id, target_user_id)


def friend_user(session: Session, current_user_id: str, target_user_id: str) -> str:
    service = RelationshipService(session)
    return service.friend_user(current_user_id, target_user_id)