"""empty message

Revision ID: 0b5e7db16af8
Revises: 0d3b152688fe
Create Date: 2024-02-07 11:37:07.698058

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import OperationalError


# revision identifiers, used by Alembic.
revision = '0b5e7db16af8'
down_revision = '0d3b152688fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        op.create_table('history',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('session_id', sa.Integer(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
    except OperationalError:
        print("Table 'history' already exist")

    try:
        with op.batch_alter_table('history', schema=None) as batch_op:
            batch_op.create_index(batch_op.f('ix_history_session_id'), ['session_id'], unique=False)
    except OperationalError:
        print("Index already exist for history")

    try:
        with op.batch_alter_table('session', schema=None) as batch_op:
            batch_op.add_column(sa.Column('nb_errors', sa.Integer(), nullable=True))
            batch_op.create_index(batch_op.f('ix_session_uuid'), ['uuid'], unique=True)
            batch_op.create_index(batch_op.f('ix_session_nb_errors'), ['nb_errors'], unique=False)
    except OperationalError:
        print("Column 'nb_errors' already exist in 'session'")

    try:
        with op.batch_alter_table('session', schema=None) as batch_op:
            batch_op.drop_index('ix_session_uuid')
    except OperationalError:
        print("Index already dropped from session")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_session_nb_errors'))
        batch_op.drop_index(batch_op.f('ix_session_uuid'))
        batch_op.create_index('ix_session_uuid', ['uuid'], unique=False)
        batch_op.drop_column('nb_errors')

    with op.batch_alter_table('history', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_history_session_id'))

    op.drop_table('history')
    # ### end Alembic commands ###
