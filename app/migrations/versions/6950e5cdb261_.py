"""empty message

Revision ID: 6950e5cdb261
Revises: f1d74162b600
Create Date: 2024-09-04 21:08:12.336009

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6950e5cdb261"
down_revision: Union[str, None] = "f1d74162b600"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "cart",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("course_id", sa.BigInteger(), nullable=False),
        sa.Column("is_selected", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["course_id"], ["course.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user_account.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("user_id", "course_id"),
    )
    op.drop_index("ix_category_slug", table_name="category")
    op.drop_column("category", "slug")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "category",
        sa.Column("slug", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.create_index("ix_category_slug", "category", ["slug"], unique=True)
    op.drop_table("cart")
    # ### end Alembic commands ###
