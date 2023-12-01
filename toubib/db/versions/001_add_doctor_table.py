"""Add doctor table

Revision ID: 001
Revises:
Create Date: 2021-06-02 14:31:33.813799

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "doctor",
        sa.Column(
            "id", sa.Integer, sa.Identity(always=True), nullable=False, primary_key=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.current_timestamp(),
            nullable=False,
        ),
        sa.Column("first_name", sa.String, nullable=False),
        sa.Column("last_name", sa.String, nullable=False),
        sa.Column("hiring_date", sa.Date, nullable=False),
        sa.Column("specialization", sa.String, nullable=False),
    )


def downgrade():
    op.drop_table("doctor")
