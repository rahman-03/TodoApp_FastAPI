"""create phone no col for users

Revision ID: c3c88e6208aa
Revises: 
Create Date: 2025-10-29 10:32:03.424915

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae75201a0b82'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('user', sa.Column('phone_no', sa.String(255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user', 'phone_no')
