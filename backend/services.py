from dataclasses import dataclass

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.repositories import RelationshipRepository


@dataclass(slots=True)
class RelationshipService:
    session: Session

    def __post_init__(self) -> None:
        self.repo = RelationshipRepository(self.session)

    def like_user(self, current_user_id: str, target_user_id: str) -> str:
        self._validate_pair(current_user_id, target_user_id)
        partner_id = self.repo.get_active_commitment_partner(current_user_id)
        target_partner_id = self.repo.get_active_commitment_partner(target_user_id)
        if partner_id is not None and partner_id != target_user_id:
            raise HTTPException(status_code=400, detail="You are already committed to someone else")

        if not self.repo.has_like(current_user_id, target_user_id):
            self.repo.create_like(current_user_id, target_user_id)

        if self.repo.has_like(target_user_id, current_user_id):
            if partner_id is None and target_partner_id is None and not self.repo.has_commitment(current_user_id, target_user_id):
                self.repo.create_commitment(current_user_id, target_user_id)
            self.repo.create_friendship(current_user_id, target_user_id)
            self.repo.remove_like(current_user_id, target_user_id)
            self.repo.remove_like(target_user_id, current_user_id)
            self.session.flush()
            return "mutual_like"

        self.session.flush()
        return "like_stored"

    def friend_user(self, current_user_id: str, target_user_id: str) -> str:
        self._validate_pair(current_user_id, target_user_id)
        if not self.repo.has_friend_request(current_user_id, target_user_id):
            self.repo.create_friend_request(current_user_id, target_user_id)

        if self.repo.has_friend_request(target_user_id, current_user_id) or self.repo.has_like(target_user_id, current_user_id):
            if not self.repo.has_friendship(current_user_id, target_user_id):
                self.repo.create_friendship(current_user_id, target_user_id)
            self.repo.remove_friend_request(current_user_id, target_user_id)
            self.repo.remove_friend_request(target_user_id, current_user_id)
            self.session.flush()
            return "friendship_created"

        self.session.flush()
        return "request_stored"

    def _validate_pair(self, current_user_id: str, target_user_id: str) -> None:
        if current_user_id == target_user_id:
            raise HTTPException(status_code=400, detail="Cannot act on yourself")
