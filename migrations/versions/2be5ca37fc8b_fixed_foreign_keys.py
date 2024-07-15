"""Fixed foreign keys.

Revision ID: 2be5ca37fc8b
Revises: 922eebbca3d9
Create Date: 2024-07-09 02:50:26.721312

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '2be5ca37fc8b'
down_revision = '922eebbca3d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role_id', sa.Integer(), nullable=False))
        if not isinstance(op.get_bind().dialect, sqlite.dialect):
            batch_op.create_foreign_key(None, 'role', ['role_id'], ['role_id'])
        else:
            batch_op.create_foreign_key('fk_user_role', 'role', ['role_id'], ['role_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        if not isinstance(op.get_bind().dialect, sqlite.dialect):
            batch_op.drop_constraint(None, type_='foreignkey')
        else:
            batch_op.drop_constraint('fk_user_role', type_='foreignkey')
        batch_op.drop_column('role_id')
    # ### end Alembic commands ###