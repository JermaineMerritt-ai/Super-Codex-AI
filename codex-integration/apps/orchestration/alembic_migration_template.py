"""<short_description_of_change>"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = '<unique_id_here>'
down_revision = '<previous_revision_id>'
branch_labels = None
depends_on = None

def upgrade():
    # Ritual of Expansion
    op.create_table(
        'example_table',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

def downgrade():
    # Ritual of Reversal
    op.drop_table('example_table')
