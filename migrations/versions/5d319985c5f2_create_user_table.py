"""Create user table

Revision ID: 5d319985c5f2
Revises: 
Create Date: 2025-01-04 19:10:25.736507

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5d319985c5f2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("xp", sa.Float(), nullable=False),
        sa.Column("xp_required", sa.Float(), nullable=False),
        sa.Column("total_xp", sa.Float(), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user")
    # ### end Alembic commands ###
