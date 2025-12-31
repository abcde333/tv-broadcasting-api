def upgrade() -> None:
    # Add a new column 'launch_year' to satellites
    op.add_column('satellites', sa.Column('launch_year', sa.Integer(), nullable=True))
    
    # Add a new column 'website' to tv_channels
    op.add_column('tv_channels', sa.Column('website', sa.String(length=255), nullable=True))
    
    # Create an index on tv_channels.country
    op.create_index('ix_tv_channels_country', 'tv_channels', ['country'])


def downgrade() -> None:
    # Remove the index
    op.drop_index('ix_tv_channels_country', table_name='tv_channels')
    
    # Remove the added columns
    op.drop_column('tv_channels', 'website')
    op.drop_column('satellites', 'launch_year')
