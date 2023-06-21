"""date

Revision ID: cce7e3dff7b7
Revises: 98c116d7d858
Create Date: 2023-06-21 09:19:24.582114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cce7e3dff7b7'
down_revision = '98c116d7d858'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('reservations', schema=None) as batch_op:
        batch_op.alter_column('party_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('party_size',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('reservation_date',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.alter_column('location_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('customer_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_constraint('uq_reservations_location_id', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservations', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_reservations_location_id', ['location_id', 'customer_id', 'reservation_date'])
        batch_op.alter_column('customer_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('location_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('reservation_date',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.alter_column('party_size',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('party_name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
