"""add cascade delete to todos

Revision ID: b815695d18b3
Revises: ae75201a0b82
Create Date: 2026-02-08 14:15:26.845015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b815695d18b3'
down_revision: Union[str, Sequence[str], None] = 'ae75201a0b82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop existing FK
    op.drop_constraint(
        constraint_name="todo_owner_id_fkey",
        table_name="todo",
        type_="foreignkey"
    )

    # Recreate FK with CASCADE
    op.create_foreign_key(
        constraint_name="fk_todo_owner_user",
        source_table="todo",
        referent_table="user",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop CASCADE FK
    op.drop_constraint(
        constraint_name="fk_todo_owner_user",
        table_name="todo",
        type_="foreignkey"
    )

    # Recreate original FK (no cascade)
    op.create_foreign_key(
        constraint_name="todo_owner_id_fkey",
        source_table="todo",
        referent_table="user",
        local_cols=["owner_id"],
        remote_cols=["id"]
    )
