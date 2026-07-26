"""initial_schema

Revision ID: 4120c8e17ab2
Revises: None
Create Date: 2026-07-25 18:23:04.779986

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '4120c8e17ab2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(op.f('calendar_events_activity_id_key'), 'calendar_events', type_='unique')
    op.create_unique_constraint(op.f('uq_calendar_events_activity_id'), 'calendar_events', ['activity_id'])
    op.drop_constraint(op.f('user_preferences_user_id_key'), 'user_preferences', type_='unique')
    op.create_unique_constraint(op.f('uq_user_preferences_user_id'), 'user_preferences', ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_constraint(op.f('uq_user_preferences_user_id'), 'user_preferences', type_='unique')
    op.create_unique_constraint(op.f('user_preferences_user_id_key'), 'user_preferences', ['user_id'], postgresql_nulls_not_distinct=False)
    op.drop_constraint(op.f('uq_calendar_events_activity_id'), 'calendar_events', type_='unique')
    op.create_unique_constraint(op.f('calendar_events_activity_id_key'), 'calendar_events', ['activity_id'], postgresql_nulls_not_distinct=False)
    # ### end Alembic commands ###