from pydantic import BaseModel, Field


class RelationshipResponse(BaseModel):
    status: str
    details: str | None = None


class UserProfileOut(BaseModel):
    id: str
    name: str | None = None
    age: int | None = None
    height: int | None = None
    state: str | None = None
    education: str | None = None
    bio: str | None = None
    committed_to_id: str | None = None


class UserProfileUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=120)
    height: int | None = Field(default=None, ge=0, le=300)
    state: str | None = Field(default=None, max_length=80)
    education: str | None = Field(default=None, max_length=120)
    bio: str | None = Field(default=None, max_length=1000)
