"""initial migration

Revision ID: 4e7f2b732770
Revises: b7980002beac
Create Date: 2019-01-07 16:08:18.654856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e7f2b732770'
down_revision = 'b7980002beac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_tests_email', table_name='tests')
    op.drop_index('ix_tests_username', table_name='tests')
    op.drop_table('tests')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tests',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=64), nullable=True),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tests_username', 'tests', ['username'], unique=1)
    op.create_index('ix_tests_email', 'tests', ['email'], unique=1)
    # ### end Alembic commands ###
