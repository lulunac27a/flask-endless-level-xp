"""Add time multiplier

Revision ID: 90e9dc716399
Revises: a5e285045629
Create Date: 2025-01-20 18:06:55.299473

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "90e9dc716399"
down_revision = "a5e285045629"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "last_time_clicked",
                sa.DateTime(),
                server_default="CURRENT_TIMESTAMP",
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column(
                "time_multiplier", sa.Integer(), server_default="1", nullable=False
            )
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("time_multiplier")
        batch_op.drop_column("last_time_clicked")

    # ### end Alembic commands ###
