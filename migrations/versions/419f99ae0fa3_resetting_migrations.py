"""Resetting migrations

Revision ID: 419f99ae0fa3
Revises: 1fe3ba8bc9f3
Create Date: 2024-10-15 20:15:01.147426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '419f99ae0fa3'
down_revision = '1fe3ba8bc9f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('image_url', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='items_pkey'),
    sa.UniqueConstraint('name', name='items_name_key')
    )
    # ### end Alembic commands ###
