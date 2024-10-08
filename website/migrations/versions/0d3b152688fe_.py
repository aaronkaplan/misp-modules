"""empty message

Revision ID: 0d3b152688fe
Revises: 0c02b861944b
Create Date: 2024-02-07 11:08:00.337971

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import OperationalError


# revision identifiers, used by Alembic.
revision = '0d3b152688fe'
down_revision = '0c02b861944b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        with op.batch_alter_table('session', schema=None) as batch_op:
            batch_op.add_column(sa.Column('glob_query', sa.String(), nullable=True))
            batch_op.add_column(sa.Column('query', sa.String(), nullable=True))
            batch_op.add_column(sa.Column('input_query', sa.String(), nullable=True))
            batch_op.add_column(sa.Column('config_module', sa.String(), nullable=True))
            batch_op.add_column(sa.Column('result', sa.String(), nullable=True))
    except OperationalError:
        print("Columns already exist in 'session'")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.drop_column('result')
        batch_op.drop_column('config_module')
        batch_op.drop_column('input_query')
        batch_op.drop_column('query')
        batch_op.drop_column('glob_query')

    # ### end Alembic commands ###
