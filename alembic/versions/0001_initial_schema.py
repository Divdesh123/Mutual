"""Initial schema.

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-06-16 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("state", sa.String(length=80), nullable=True),
        sa.Column("education", sa.String(length=120), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("committed_to_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "romantic_likes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("from_user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("to_user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("from_user_id", "to_user_id", name="uq_romantic_like_pair"),
    )
    op.create_index("ix_romantic_likes_to_user_id", "romantic_likes", ["to_user_id"])
    op.create_index("ix_romantic_likes_from_user_id", "romantic_likes", ["from_user_id"])

    op.create_table(
        "friend_requests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("from_user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("to_user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("from_user_id", "to_user_id", name="uq_friend_request_pair"),
    )
    op.create_index("ix_friend_requests_to_user_id", "friend_requests", ["to_user_id"])
    op.create_index("ix_friend_requests_from_user_id", "friend_requests", ["from_user_id"])

    op.create_table(
        "friendships",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_low_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("user_high_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_low_id", "user_high_id", name="uq_friendship_pair"),
    )
    op.create_index("ix_friendships_user_low_id", "friendships", ["user_low_id"])
    op.create_index("ix_friendships_user_high_id", "friendships", ["user_high_id"])

    op.create_table(
        "commitments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_low_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("user_high_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_low_id", "user_high_id", name="uq_commitment_pair"),
    )
    op.create_index("ix_commitments_user_low_id", "commitments", ["user_low_id"])
    op.create_index("ix_commitments_user_high_id", "commitments", ["user_high_id"])


def downgrade() -> None:
    op.drop_index("ix_commitments_user_high_id", table_name="commitments")
    op.drop_index("ix_commitments_user_low_id", table_name="commitments")
    op.drop_table("commitments")

    op.drop_index("ix_friendships_user_high_id", table_name="friendships")
    op.drop_index("ix_friendships_user_low_id", table_name="friendships")
    op.drop_table("friendships")

    op.drop_index("ix_friend_requests_from_user_id", table_name="friend_requests")
    op.drop_index("ix_friend_requests_to_user_id", table_name="friend_requests")
    op.drop_table("friend_requests")

    op.drop_index("ix_romantic_likes_from_user_id", table_name="romantic_likes")
    op.drop_index("ix_romantic_likes_to_user_id", table_name="romantic_likes")
    op.drop_table("romantic_likes")

    op.drop_table("users")
