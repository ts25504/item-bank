"""initial migration

Revision ID: 1ce02e4ebef9
Revises: 24ca29c0ff38
Create Date: 2015-04-14 15:55:56.029034

"""

# revision identifiers, used by Alembic.
revision = '1ce02e4ebef9'
down_revision = '24ca29c0ff38'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blank_fill', sa.Column('knowledge_points_name', sa.String(length=127), nullable=True))
    op.add_column('essay', sa.Column('knowledge_points_name', sa.String(length=127), nullable=True))
    op.add_column('single_choice', sa.Column('knowledge_points_name', sa.String(length=127), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('single_choice', 'knowledge_points_name')
    op.drop_column('essay', 'knowledge_points_name')
    op.drop_column('blank_fill', 'knowledge_points_name')
    ### end Alembic commands ###
