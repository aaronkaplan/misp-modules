"""empty message

Revision ID: 1d38ae8361a7
Revises: 0b5e7db16af8
Create Date: 2024-02-07 11:44:30.236490

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import OperationalError


# revision identifiers, used by Alembic.
revision = '1d38ae8361a7'
down_revision = '0b5e7db16af8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        op.create_table('session_db',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('uuid', sa.String(length=36), nullable=True),
            sa.Column('glob_query', sa.String(), nullable=True),
            sa.Column('query', sa.String(), nullable=True),
            sa.Column('input_query', sa.String(), nullable=True),
            sa.Column('config_module', sa.String(), nullable=True),
            sa.Column('result', sa.String(), nullable=True),
            sa.Column('nb_errors', sa.Integer(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
    except OperationalError:
        print("Table 'session_db' already exist")

    try:
        with op.batch_alter_table('session_db', schema=None) as batch_op:
            batch_op.create_index(batch_op.f('ix_session_db_nb_errors'), ['nb_errors'], unique=False)
            batch_op.create_index(batch_op.f('ix_session_db_uuid'), ['uuid'], unique=True)
    except OperationalError:
        print("Index already exist in 'session_db'")

    try:
        with op.batch_alter_table('session', schema=None) as batch_op:
            batch_op.drop_index('ix_session_nb_errors')
            batch_op.drop_index('ix_session_uuid')
    except OperationalError:
        print("Index already dropped from 'session'")

    try:
        op.drop_table('session')
    except OperationalError:
        print("Table 'session' already dropped")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('session',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=True),
    sa.Column('glob_query', sa.VARCHAR(), nullable=True),
    sa.Column('query', sa.VARCHAR(), nullable=True),
    sa.Column('input_query', sa.VARCHAR(), nullable=True),
    sa.Column('config_module', sa.VARCHAR(), nullable=True),
    sa.Column('result', sa.VARCHAR(), nullable=True),
    sa.Column('nb_errors', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.create_index('ix_session_uuid', ['uuid'], unique=1)
        batch_op.create_index('ix_session_nb_errors', ['nb_errors'], unique=False)

    with op.batch_alter_table('session_db', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_session_db_uuid'))
        batch_op.drop_index(batch_op.f('ix_session_db_nb_errors'))

    op.drop_table('session_db')
    # ### end Alembic commands ###
