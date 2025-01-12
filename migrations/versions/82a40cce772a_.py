"""empty message

Revision ID: 82a40cce772a
Revises: 94a9fff99f98
Create Date: 2021-04-05 17:07:21.565786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "82a40cce772a"
down_revision = "94a9fff99f98"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
