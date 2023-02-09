"""Link Users and Posts Table

Revision ID: cb3a9ec614d9
Revises: 2071b759a4d3
Create Date: 2023-02-09 17:24:28.151375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb3a9ec614d9'
down_revision = '2071b759a4d3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("owner_id", sa.Integer(),
                            sa.ForeignKey("users.id", ondelete="CASCADE"),
                            nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "owner_id")
