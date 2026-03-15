"""add_from_name_and_array_to_email_to_email_messages

Revision ID: a1b2c3d4e5f6
Revises: c08f9c548cfa
Create Date: 2026-03-14 00:00:00.000000+00:00

"""

from typing import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: str | None = "c08f9c548cfa"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TABLE email_messages ALTER COLUMN to_email TYPE TEXT[] USING ARRAY[to_email]")
    op.add_column("email_messages", sa.Column("from_name", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("email_messages", "from_name")
    op.execute("ALTER TABLE email_messages ALTER COLUMN to_email TYPE TEXT USING to_email[1]")
