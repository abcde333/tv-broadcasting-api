from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '313c619969b8'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('satellites', sa.Column('launch_year', sa.Integer(), nullable=True))
    op.add_column('tv_channels', sa.Column('website', sa.String(length=255), nullable=True))
    op.create_index('ix_tv_channels_country', 'tv_channels', ['country'])


def downgrade():
    op.drop_index('ix_tv_channels_country', table_name='tv_channels')
    op.drop_column('tv_channels', 'website')
    op.drop_column('satellites', 'launch_year')
