"""add new table themes

Revision ID: 902b3bb65003
Revises: 4c54b0d878fd
Create Date: 2020-12-21 19:36:33.195000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '902b3bb65003'
down_revision = '4c54b0d878fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('themes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('themes')
    # ### end Alembic commands ###
