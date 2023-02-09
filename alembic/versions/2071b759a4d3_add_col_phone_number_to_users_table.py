"""Add Col Phone Number to Users Table

Revision ID: 2071b759a4d3
Revises: f8325edcb8ad
Create Date: 2023-02-09 16:45:07.430037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2071b759a4d3'
down_revision = 'f8325edcb8ad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
