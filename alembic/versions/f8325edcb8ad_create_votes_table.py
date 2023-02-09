"""Create Votes Table

Revision ID: f8325edcb8ad
Revises: ed124ede88be
Create Date: 2023-02-09 16:24:25.103369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8325edcb8ad'
down_revision = 'ed124ede88be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("votes",
                    sa.Column("user_id", sa.Integer(),
                              sa.ForeignKey("users.id", ondelete="CASCADE"),
                              primary_key=True, nullable=False),
                    sa.Column("post_id", sa.Integer(),
                              sa.ForeignKey("posts.id", ondelete="CASCADE"),
                              primary_key=True, nullable=False))


def downgrade() -> None:
    op.drop_table("votes")
