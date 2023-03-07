"""add content column to post table

Revision ID: 07d9c990fd93
Revises: 5fbf67622be1
Create Date: 2023-03-06 15:38:29.546971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07d9c990fd93'
down_revision = '5fbf67622be1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
