"""create_slides_table

Revision ID: a1b2c3d4e5f6
Revises: 47288aa62bf8
Create Date: 2026-11-08 21:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "47288aa62bf8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "slides",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("kicker", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("cta_label", sa.String(length=80), nullable=False),
        sa.Column("cta_to", sa.String(length=255), nullable=False),
        sa.Column("image", sa.String(length=255), nullable=False),
        sa.Column("image_position", sa.String(length=80), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_slides_sort_order"), "slides", ["sort_order"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_slides_sort_order"), table_name="slides")
    op.drop_table("slides")
