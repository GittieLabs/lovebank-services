"""empty message

Revision ID: 0b1d12aa49b0
Revises: 2aba7fc1308d
Create Date: 2020-06-09 17:17:14.233322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b1d12aa49b0'
down_revision = '2aba7fc1308d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    # ### end Alembic commands ###
