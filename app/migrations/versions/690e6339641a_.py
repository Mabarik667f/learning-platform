"""empty message

Revision ID: 690e6339641a
Revises: 657bd3af8ddc
Create Date: 2024-09-28 23:54:21.127017

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "690e6339641a"
down_revision: Union[str, None] = "657bd3af8ddc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("subsection", "number")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "subsection",
        sa.Column("number", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    # ### end Alembic commands ###
