"""agrega columna stock en productos

Revision ID: c1a4d6e9f302
Revises: 2bfd7802b5ae
Create Date: 2026-06-20 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c1a4d6e9f302"
down_revision: str | Sequence[str] | None = "2bfd7802b5ae"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "productos",
        sa.Column("stock", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("productos", "stock")
