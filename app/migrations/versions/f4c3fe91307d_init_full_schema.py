"""init full schema

Revision ID: f4c3fe91307d
Revises: df21472fa316
Create Date: 2026-02-28 21:01:51.725910

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4c3fe91307d'
down_revision: Union[str, Sequence[str], None] = 'df21472fa316'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # organizations
    op.create_table(
        'organizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('bin', sa.String(), nullable=True),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('contacts_json', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.ForeignKeyConstraint(['parent_id'], ['organizations.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('bin')
    )
    op.create_index(op.f('ix_organizations_id'), 'organizations', ['id'])

    # org_units
    op.create_table(
        'org_units',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('organization_id', sa.Integer()),
        sa.Column('parent_id', sa.Integer()),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('code', sa.String()),
        sa.Column('manager_employee_id', sa.Integer()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id']),
        sa.ForeignKeyConstraint(['parent_id'], ['org_units.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_org_units_id'), 'org_units', ['id'])

    # employees
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('organization_id', sa.Integer()),
        sa.Column('org_unit_id', sa.Integer()),
        sa.Column('employee_number', sa.String(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('middle_name', sa.String()),
        sa.Column('email', sa.String()),
        sa.Column('phone', sa.String()),
        sa.Column('position', sa.String()),
        sa.Column('grade', sa.String()),
        sa.Column('is_active', sa.Boolean()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id']),
        sa.ForeignKeyConstraint(['org_unit_id'], ['org_units.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employees_id'), 'employees', ['id'])

    # users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer()),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean()),
        sa.Column('last_login_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'])

    # roles
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String()),
        sa.Column('name', sa.String()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    op.create_index(op.f('ix_roles_id'), 'roles', ['id'])

    # training_courses
    op.create_table(
        'training_courses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('provider_id', sa.Integer()),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('type', sa.String()),
        sa.Column('description', sa.String()),
        sa.Column('is_active', sa.Boolean()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['provider_id'], ['providers.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_training_courses_id'), 'training_courses', ['id'])

    # contracts
    op.create_table(
        'contracts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('provider_id', sa.Integer()),
        sa.Column('contract_number', sa.String(), nullable=False),
        sa.Column('title', sa.String()),
        sa.Column('start_date', sa.DateTime()),
        sa.Column('end_date', sa.DateTime()),
        sa.Column('currency', sa.String()),
        sa.Column('budget_limit', sa.Numeric(14, 2)),
        sa.Column('status', sa.String()),
        sa.Column('created_by_user_id', sa.Integer()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['provider_id'], ['providers.id']),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contracts_id'), 'contracts', ['id'])

    # training_sessions
    op.create_table(
        'training_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer()),
        sa.Column('trainer_id', sa.Integer()),
        sa.Column('start_datetime', sa.DateTime()),
        sa.Column('end_datetime', sa.DateTime()),
        sa.Column('city', sa.String()),
        sa.Column('location', sa.String()),
        sa.Column('price_amount', sa.Numeric(14, 2)),
        sa.Column('currency', sa.String()),
        sa.Column('status', sa.String()),
        sa.ForeignKeyConstraint(['course_id'], ['training_courses.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_training_sessions_id'), 'training_sessions', ['id'])

    # applications
    op.create_table(
        'applications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('requested_by_user_id', sa.Integer()),
        sa.Column('organization_id', sa.Integer()),
        sa.Column('org_unit_id', sa.Integer()),
        sa.Column('course_id', sa.Integer()),
        sa.Column('status', sa.String()),
        sa.Column('comment', sa.String()),
        sa.Column('submitted_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['requested_by_user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id']),
        sa.ForeignKeyConstraint(['org_unit_id'], ['org_units.id']),
        sa.ForeignKeyConstraint(['course_id'], ['training_courses.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_applications_id'), 'applications', ['id'])

    # application_items
    op.create_table(
        'application_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('application_id', sa.Integer()),
        sa.Column('employee_id', sa.Integer()),
        sa.Column('session_id', sa.Integer()),
        sa.Column('price_amount', sa.Numeric(14, 2)),
        sa.Column('currency', sa.String()),
        sa.Column('status', sa.String()),
        sa.ForeignKeyConstraint(['application_id'], ['applications.id']),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id']),
        sa.ForeignKeyConstraint(['session_id'], ['training_sessions.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_application_items_id'), 'application_items', ['id'])

    # training_participants
    op.create_table(
        'training_participants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer()),
        sa.Column('employee_id', sa.Integer()),
        sa.Column('attendance_status', sa.String()),
        sa.ForeignKeyConstraint(['session_id'], ['training_sessions.id']),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_training_participants_id'), 'training_participants', ['id'])

    # user_roles
    op.create_table(
        'user_roles',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )

def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_training_participants_id'), table_name='training_participants')
    op.drop_table('training_participants')
    op.drop_index(op.f('ix_application_items_id'), table_name='application_items')
    op.drop_table('application_items')
    op.drop_table('user_roles')
    op.drop_index(op.f('ix_training_sessions_id'), table_name='training_sessions')
    op.drop_table('training_sessions')
    op.drop_index(op.f('ix_contracts_id'), table_name='contracts')
    op.drop_table('contracts')
    op.drop_index(op.f('ix_applications_id'), table_name='applications')
    op.drop_table('applications')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_training_courses_id'), table_name='training_courses')
    op.drop_table('training_courses')
    op.drop_index(op.f('ix_roles_id'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_organizations_id'), table_name='organizations')
    op.drop_table('organizations')
    op.drop_index(op.f('ix_org_units_id'), table_name='org_units')
    op.drop_table('org_units')
    op.drop_index(op.f('ix_employees_id'), table_name='employees')
    op.drop_table('employees')
    # ### end Alembic commands ###
