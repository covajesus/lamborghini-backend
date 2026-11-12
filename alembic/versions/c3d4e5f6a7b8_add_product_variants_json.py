"""add_product_variants_json

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-11-09 11:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c3d4e5f6a7b8"
down_revision: Union[str, Sequence[str], None] = "b2c3d4e5f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products", sa.Column("options", sa.JSON(), nullable=True))
    op.add_column("products", sa.Column("color_images", sa.JSON(), nullable=True))
    op.add_column("products", sa.Column("variants", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("products", "variants")
    op.drop_column("products", "color_images")
    op.drop_column("products", "options")
