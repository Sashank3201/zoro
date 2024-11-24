from alembic import op
import sqlalchemy as sa

def upgrade():
    # Drop the is_admin column from the user table
    with op.batch_alter_table('user') as batch_op:
        batch_op.drop_column('is_admin')

def downgrade():
    # Add back the is_admin column
    with op.batch_alter_table('user') as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=True, default=False))
