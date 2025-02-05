"""empty message

Revision ID: d06a02684b1f
Revises: ee9dc5c95793
Create Date: 2024-02-27 15:10:14.310455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd06a02684b1f'
down_revision = 'ee9dc5c95793'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)
        batch_op.alter_column('gender',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=250),
               nullable=True)

    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.alter_column('gender',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(length=250),
               nullable=False)

    # ### end Alembic commands ###
