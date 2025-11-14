# alembic/versions/20251112_init_schema.py
from alembic import op
import sqlalchemy as sa

revision = "20251112_init"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "contributors",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("roles", sa.JSON, nullable=False),
        sa.Column("seal", sa.String(256), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )
    op.create_table(
        "scrolls",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("contributor_id", sa.Integer, sa.ForeignKey("contributors.id")),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )
    op.create_table(
        "capsules",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("type", sa.String(100), nullable=False),
        sa.Column("payload", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("payload", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )
    op.create_table(
        "replay_archives",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("tag", sa.String(100), nullable=False),
        sa.Column("data", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )

def downgrade():
    op.drop_table("replay_archives")
    op.drop_table("audit_logs")
    op.drop_table("capsules")
    op.drop_table("scrolls")
    op.drop_table("contributors")