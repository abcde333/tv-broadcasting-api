"""add index to broadcasts frequency

Revision ID: 5616ac735614
Revises: 313c619969b8
Create Date: 2025-12-31 15:14:54.211301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5616ac735614'
down_revision: Union[str, Sequence[str], None] = '313c619969b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(
        'ix_broadcasts_frequency',
        'broadcasts',
        ['frequency']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        'ix_broadcasts_frequency',
        table_name='broadcasts'
    )

