"""add user table

Revision ID: 9099a847fe4c
Revises: 07d9c990fd93
Create Date: 2023-03-06 15:57:04.615056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9099a847fe4c'
down_revision = '07d9c990fd93'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                   sa.Column('id', sa.Integer(), nullable=False),
                   sa.Column('email', sa.String(), nullable=False),
                   sa.Column('password', sa.String(), nullable=False),
                   sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                        nullable=False),
                   sa.PrimaryKeyConstraint('id'),
                   sa.UniqueConstraint('email')
                   )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
