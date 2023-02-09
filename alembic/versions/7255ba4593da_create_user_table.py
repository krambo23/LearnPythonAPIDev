"""Create User Table

Revision ID: 7255ba4593da
Revises: 
Create Date: 2023-02-09 16:18:54.825737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7255ba4593da'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
                    sa.Column("email", sa.String(), unique=True, nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("NOW()"), nullable=False))


def downgrade() -> None:
    op.drop_table("users")
