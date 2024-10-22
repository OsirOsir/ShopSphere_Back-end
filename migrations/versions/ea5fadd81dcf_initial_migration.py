"""Initial migration

Revision ID: ea5fadd81dcf
Revises: 
Create Date: 2024-10-22 08:43:12.047155

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ea5fadd81dcf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Remove the line that drops the orders table
    # op.drop_table('orders')

    # Update the cart_items table
    with op.batch_alter_table('cart_items', schema=None) as batch_op:
        # Drop the foreign key constraint
        batch_op.drop_constraint('fk_cart_items_order_id_orders', type_='foreignkey')
        # Drop the order_id column
        batch_op.drop_column('order_id')

    # Update the items table
    with op.batch_alter_table('items', schema=None) as batch_op:
        # Add the is_flash_sale column
        batch_op.add_column(sa.Column('is_flash_sale', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('is_flash_sale')

    with op.batch_alter_table('cart_items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('fk_cart_items_order_id_orders', 'orders', ['order_id'], ['id'])

    op.create_table('orders',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('total_price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_orders_user_id_users'),
        sa.PrimaryKeyConstraint('id', name='orders_pkey')
    )
    # ### end Alembic commands ###
