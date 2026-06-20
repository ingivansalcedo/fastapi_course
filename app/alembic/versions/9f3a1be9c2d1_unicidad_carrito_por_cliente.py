"""unicidad carrito por cliente

Revision ID: 9f3a1be9c2d1
Revises: 6bca4f5c781e
Create Date: 2026-06-17 16:20:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9f3a1be9c2d1"
down_revision: Union[str, Sequence[str], None] = "6bca4f5c781e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Si existen carritos duplicados por cliente, conservamos el de menor id.
    op.execute(
        """
        UPDATE items_carrito AS ic
        SET carrito_id = d.keep_id
        FROM (
            SELECT id, MIN(id) OVER (PARTITION BY cliente_id) AS keep_id
            FROM carrito
            WHERE cliente_id IS NOT NULL
        ) AS d
        WHERE ic.carrito_id = d.id
          AND d.id <> d.keep_id
        """
    )

    op.execute(
        """
        DELETE FROM carrito AS c
        USING (
            SELECT id, MIN(id) OVER (PARTITION BY cliente_id) AS keep_id
            FROM carrito
            WHERE cliente_id IS NOT NULL
        ) AS d
        WHERE c.id = d.id
          AND d.id <> d.keep_id
        """
    )

    op.create_unique_constraint(
        "uq_carrito_cliente_id",
        "carrito",
        ["cliente_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_carrito_cliente_id", "carrito", type_="unique")
