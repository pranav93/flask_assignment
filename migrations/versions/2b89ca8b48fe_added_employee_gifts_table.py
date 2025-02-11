"""added employee_gifts table

Revision ID: 2b89ca8b48fe
Revises: ece5e1f05b76
Create Date: 2019-12-18 10:09:30.362838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b89ca8b48fe'
down_revision = 'ece5e1f05b76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee_gifts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee_id', sa.Integer(), nullable=False),
    sa.Column('gift_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
    sa.ForeignKeyConstraint(['gift_id'], ['gifts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employee_gifts')
    # ### end Alembic commands ###
