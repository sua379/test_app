"""'adding_the_username'

Revision ID: 114f7d561930
Revises: 13cf7202d10f
Create Date: 2022-08-09 13:40:51.876400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '114f7d561930'
down_revision = '13cf7202d10f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('db_model', sa.Column('username', sa.String(length=50), nullable=False))
    op.create_unique_constraint(None, 'db_model', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'db_model', type_='unique')
    op.drop_column('db_model', 'username')
    # ### end Alembic commands ###
