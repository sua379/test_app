"""'added_the_post_table'

Revision ID: 13cf7202d10f
Revises: 
Create Date: 2022-08-05 14:29:07.646909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13cf7202d10f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Title', sa.String(length=200), nullable=False),
    sa.Column('Author', sa.String(length=200), nullable=False),
    sa.Column('Slug', sa.String(length=200), nullable=False),
    sa.Column('Blog_content', sa.Text(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('Slug')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###