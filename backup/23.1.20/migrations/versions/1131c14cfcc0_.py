"""empty message

Revision ID: 1131c14cfcc0
Revises: 7fd6ce8e3f08
Create Date: 2020-01-23 00:47:32.710116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1131c14cfcc0'
down_revision = '7fd6ce8e3f08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.create_foreign_key(None, 'cart', 'products', ['product_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.create_foreign_key(None, 'cart', 'buyers', ['product_id'], ['id'])
    # ### end Alembic commands ###
