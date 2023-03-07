"""add foreign key to post table

Revision ID: 93c6337d2b85
Revises: 9099a847fe4c
Create Date: 2023-03-06 16:06:37.931448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93c6337d2b85'
down_revision = '9099a847fe4c'
branch_labels = None
depends_on = None

POST_TABLE="posts"

def upgrade() -> None:
    op.add_column(POST_TABLE, sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table=POST_TABLE, referent_table="users",
        local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name=POST_TABLE)
    op.drop_column(POST_TABLE, "owner_id")
    pass
