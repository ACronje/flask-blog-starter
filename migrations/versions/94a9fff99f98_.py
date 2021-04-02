"""empty message

Revision ID: 94a9fff99f98
Revises: 536f1609caed
Create Date: 2021-04-03 00:11:40.057371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "94a9fff99f98"
down_revision = "536f1609caed"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(collation="NOCASE"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "posttags",
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tags.id"],
        ),
        sa.PrimaryKeyConstraint("post_id", "tag_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("posttags")
    op.drop_table("tags")
    # ### end Alembic commands ###
