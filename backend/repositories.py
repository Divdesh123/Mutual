from datetime import datetime, timezone

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from backend.models import Commitment, FriendRequest, Friendship, RomanticLike, User


class RelationshipRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, user_id: str) -> User | None:
        return self.session.get(User, user_id)

    def get_active_commitment_partner(self, user_id: str) -> str | None:
        stmt = select(Commitment).where(
            Commitment.ended_at.is_(None),
            or_(Commitment.user_low_id == user_id, Commitment.user_high_id == user_id),
        )
        commitment = self.session.execute(stmt).scalar_one_or_none()
        if commitment is None:
            return None
        return commitment.user_high_id if commitment.user_low_id == user_id else commitment.user_low_id

    def has_like(self, from_user_id: str, to_user_id: str) -> bool:
        stmt = select(RomanticLike.id).where(
            RomanticLike.from_user_id == from_user_id,
            RomanticLike.to_user_id == to_user_id,
        )
        return self.session.execute(stmt).first() is not None

    def has_friend_request(self, from_user_id: str, to_user_id: str) -> bool:
        stmt = select(FriendRequest.id).where(
            FriendRequest.from_user_id == from_user_id,
            FriendRequest.to_user_id == to_user_id,
        )
        return self.session.execute(stmt).first() is not None

    def has_friendship(self, user_a_id: str, user_b_id: str) -> bool:
        low_id, high_id = sorted((user_a_id, user_b_id))
        stmt = select(Friendship.id).where(
            Friendship.user_low_id == low_id,
            Friendship.user_high_id == high_id,
        )
        return self.session.execute(stmt).first() is not None

    def has_commitment(self, user_a_id: str, user_b_id: str) -> bool:
        low_id, high_id = sorted((user_a_id, user_b_id))
        stmt = select(Commitment.id).where(
            Commitment.user_low_id == low_id,
            Commitment.user_high_id == high_id,
            Commitment.ended_at.is_(None),
        )
        return self.session.execute(stmt).first() is not None

    def create_like(self, from_user_id: str, to_user_id: str) -> RomanticLike:
        like = RomanticLike(from_user_id=from_user_id, to_user_id=to_user_id)
        self.session.add(like)
        return like

    def create_friend_request(self, from_user_id: str, to_user_id: str) -> FriendRequest:
        request = FriendRequest(from_user_id=from_user_id, to_user_id=to_user_id)
        self.session.add(request)
        return request

    def create_friendship(self, user_a_id: str, user_b_id: str) -> Friendship:
        low_id, high_id = sorted((user_a_id, user_b_id))
        friendship = Friendship(user_low_id=low_id, user_high_id=high_id)
        self.session.add(friendship)
        return friendship

    def create_commitment(self, user_a_id: str, user_b_id: str) -> Commitment:
        low_id, high_id = sorted((user_a_id, user_b_id))
        commitment = Commitment(user_low_id=low_id, user_high_id=high_id)
        self.session.add(commitment)
        return commitment

    def end_commitment(self, user_a_id: str, user_b_id: str) -> Commitment | None:
        low_id, high_id = sorted((user_a_id, user_b_id))
        stmt = select(Commitment).where(
            Commitment.user_low_id == low_id,
            Commitment.user_high_id == high_id,
            Commitment.ended_at.is_(None),
        )
        commitment = self.session.execute(stmt).scalar_one_or_none()
        if commitment is None:
            return None
        commitment.ended_at = datetime.now(timezone.utc)
        return commitment

    def remove_friend_request(self, from_user_id: str, to_user_id: str) -> None:
        stmt = select(FriendRequest).where(
            FriendRequest.from_user_id == from_user_id,
            FriendRequest.to_user_id == to_user_id,
        )
        for request in self.session.execute(stmt).scalars().all():
            self.session.delete(request)

    def remove_like(self, from_user_id: str, to_user_id: str) -> None:
        stmt = select(RomanticLike).where(
            RomanticLike.from_user_id == from_user_id,
            RomanticLike.to_user_id == to_user_id,
        )
        for like in self.session.execute(stmt).scalars().all():
            self.session.delete(like)
