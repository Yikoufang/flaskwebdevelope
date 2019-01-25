"""initial migration

Revision ID: 0bcdac1417b9
Revises: fef955b6b2b5
Create Date: 2019-01-07 16:26:37.397417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bcdac1417b9'
down_revision = 'fef955b6b2b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('postsss')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('postsss',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
