"""person

Revision ID: d272357686e6
Revises: fe4331f34d54
Create Date: 2023-10-28 23:33:38.857026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd272357686e6'
down_revision: Union[str, None] = 'fe4331f34d54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('original_name', sa.String(), nullable=True),
    sa.Column('popularity', sa.Double(), nullable=True),
    sa.Column('gender', sa.Enum('male', 'female', 'other', name='gender', native_enum=False), nullable=True),
    sa.Column('job', sa.String(), nullable=False),
    sa.Column('profile_path', sa.String(), nullable=False),
    sa.Column('movie_ids', sa.ARRAY(sa.Integer()), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('person')
    # ### end Alembic commands ###
