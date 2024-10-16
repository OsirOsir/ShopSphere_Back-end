"""Remove image_url column

Revision ID: bcdb8db405d9
Revises: ca36d43baae4
Create Date: 2024-10-15 18:53:33.482953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcdb8db405d9'
down_revision = 'ca36d43baae4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('image_url')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_url', sa.TEXT(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###