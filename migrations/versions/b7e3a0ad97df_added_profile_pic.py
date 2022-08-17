"""'ADDED_PROFILE_PIC

Revision ID: b7e3a0ad97df
Revises: 2a5d087da922
Create Date: 2022-08-15 13:44:19.311512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7e3a0ad97df'
down_revision = '2a5d087da922'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('db_model', sa.Column('profile_pic', sa.String(length=728), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('db_model', 'profile_pic')
    # ### end Alembic commands ###