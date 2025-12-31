"""add gin index for metadata json search

Revision ID: ea5806ba0752
Revises: 5616ac735614
Create Date: 2025-12-31 18:34:28.895719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea5806ba0752'
down_revision: Union[str, Sequence[str], None] = '5616ac735614'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    op.execute("""
        CREATE INDEX idx_tv_channels_metadata_trgm
        ON tv_channels
        USING gin ((metadata_json::text) gin_trgm_ops);
    """)



def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS idx_tv_channels_metadata_trgm;")
