"""Create Posts Table

Revision ID: ed124ede88be
Revises: 7255ba4593da
Create Date: 2023-02-09 16:21:51.986270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed124ede88be'
down_revision = '7255ba4593da'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts",
                    sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
                    sa.Column("title", sa.String(), nullable=False),
                    sa.Column("content", sa.String(), nullable=False),
                    sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("NOW()"), nullable=False))


def downgrade() -> None:
    op.drop_table("posts")
