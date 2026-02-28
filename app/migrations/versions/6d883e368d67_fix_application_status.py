"""fix application status

Revision ID: 6d883e368d67
Revises: 19019ff9b619
Create Date: 2026-03-01 01:32:48.624191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d883e368d67'
down_revision: Union[str, Sequence[str], None] = '19019ff9b619'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
