"""empty message

Revision ID: 30af3f699b17
Revises: 2be5ca37fc8b
Create Date: 2024-07-16 01:00:41.905432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30af3f699b17'
down_revision = '2be5ca37fc8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_user_role', 'role', ['role_id'], ['role_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('fk_user_role', type_='foreignkey')

    # ### end Alembic commands ###