"""initial migration

Revision ID: 48d34ea52bfc
Revises: 12b46f9f5af5
Create Date: 2015-04-07 01:03:43.818641

"""

# revision identifiers, used by Alembic.
revision = '48d34ea52bfc'
down_revision = '12b46f9f5af5'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blank_fill', 'faq_html')
    op.drop_column('blank_fill', 'question_html')
    op.drop_column('essay', 'faq_html')
    op.drop_column('essay', 'question_html')
    op.drop_column('essay', 'answer_html')
    op.drop_column('single_choice', 'faq_html')
    op.drop_column('single_choice', 'question_html')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('single_choice', sa.Column('question_html', mysql.TEXT(), nullable=True))
    op.add_column('single_choice', sa.Column('faq_html', mysql.TEXT(), nullable=True))
    op.add_column('essay', sa.Column('answer_html', mysql.TEXT(), nullable=True))
    op.add_column('essay', sa.Column('question_html', mysql.TEXT(), nullable=True))
    op.add_column('essay', sa.Column('faq_html', mysql.TEXT(), nullable=True))
    op.add_column('blank_fill', sa.Column('question_html', mysql.TEXT(), nullable=True))
    op.add_column('blank_fill', sa.Column('faq_html', mysql.TEXT(), nullable=True))
    ### end Alembic commands ###
