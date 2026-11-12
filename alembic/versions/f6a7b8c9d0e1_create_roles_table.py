"""create_roles_table

Revision ID: f6a7b8c9d0e1
Revises: e5f6a7b8c9d0
Create Date: 2026-11-09 12:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f6a7b8c9d0e1"
down_revision: Union[str, Sequence[str], None] = "e5f6a7b8c9d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("key", sa.String(length=60), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("color", sa.String(length=20), nullable=False),
        sa.Column("permissions", sa.JSON(), nullable=True),
        sa.Column("is_system", sa.Boolean(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("key"),
        sa.UniqueConstraint("color"),
    )
    op.create_index(op.f("ix_roles_key"), "roles", ["key"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_roles_key"), table_name="roles")
    op.drop_table("roles")
