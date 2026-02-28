-- PostgreSQL DDL for corporate offline training management
-- Notes:
-- - Uses BIGSERIAL PKs
-- - Uses TEXT enums via CHECK constraints (portable)
-- - Adds essential FK constraints and indexes
-- - Money fields are NUMERIC(14,2)
-- - If you prefer real PostgreSQL ENUM types, скажи - переделаю на CREATE TYPE.

BEGIN;

-- 1) Core org structure
CREATE TABLE organizations (
  id            BIGSERIAL PRIMARY KEY,
  parent_id     BIGINT NULL REFERENCES organizations(id) ON DELETE SET NULL,
  name          TEXT NOT NULL,
  bin           TEXT NULL,
  address       TEXT NULL,
  contacts_json JSONB NULL,
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT organizations_bin_uniq UNIQUE (bin)
);

CREATE INDEX idx_organizations_parent_id ON organizations(parent_id);

CREATE TABLE org_units (
  id                BIGSERIAL PRIMARY KEY,
  organization_id   BIGINT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  parent_id         BIGINT NULL REFERENCES org_units(id) ON DELETE SET NULL,
  name              TEXT NOT NULL,
  code              TEXT NULL,
  manager_employee_id BIGINT NULL, -- FK added after employees created
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_org_units_org_id ON org_units(organization_id);
CREATE INDEX idx_org_units_parent_id ON org_units(parent_id);

CREATE TABLE employees (
  id              BIGSERIAL PRIMARY KEY,
  organization_id BIGINT NOT NULL REFERENCES organizations(id) ON DELETE RESTRICT,
  org_unit_id     BIGINT NULL REFERENCES org_units(id) ON DELETE SET NULL,
  employee_number TEXT NULL,
  first_name      TEXT NOT NULL,
  last_name       TEXT NOT NULL,
  middle_name     TEXT NULL,
  email           TEXT NULL,
  phone           TEXT NULL,
  position        TEXT NULL,
  grade           TEXT NULL,
  is_active       BOOLEAN NOT NULL DEFAULT TRUE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT employees_org_empnum_uniq UNIQUE (organization_id, employee_number)
);

CREATE INDEX idx_employees_org_id ON employees(organization_id);
CREATE INDEX idx_employees_org_unit_id ON employees(org_unit_id);
CREATE INDEX idx_employees_email ON employees(email);

-- Now add FK for manager_employee_id
ALTER TABLE org_units
  ADD CONSTRAINT fk_org_units_manager_employee
  FOREIGN KEY (manager_employee_id) REFERENCES employees(id) ON DELETE SET NULL;

CREATE INDEX idx_org_units_manager_employee_id ON org_units(manager_employee_id);

-- 2) Users and roles
CREATE TABLE users (
  id            BIGSERIAL PRIMARY KEY,
  employee_id   BIGINT NULL REFERENCES employees(id) ON DELETE SET NULL,
  email         TEXT NOT NULL,
  password_hash TEXT NULL,
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  last_login_at TIMESTAMPTZ NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT users_email_uniq UNIQUE (email)
);

CREATE INDEX idx_users_employee_id ON users(employee_id);

CREATE TABLE roles (
  id    BIGSERIAL PRIMARY KEY,
  code  TEXT NOT NULL,
  name  TEXT NOT NULL,
  CONSTRAINT roles_code_uniq UNIQUE (code)
);

CREATE TABLE user_roles (
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role_id BIGINT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
  PRIMARY KEY (user_id, role_id)
);

CREATE INDEX idx_user_roles_role_id ON user_roles(role_id);

-- Optional seed roles
INSERT INTO roles(code, name) VALUES
  ('HR_ADMIN', 'HR Admin'),
  ('MANAGER',  'Manager'),
  ('EMPLOYEE', 'Employee')
ON CONFLICT (code) DO NOTHING;

-- 3) Providers and trainers
CREATE TABLE providers (
  id            BIGSERIAL PRIMARY KEY,
  name          TEXT NOT NULL,
  bin           TEXT NULL,
  legal_address TEXT NULL,
  contacts_json JSONB NULL,
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT providers_bin_uniq UNIQUE (bin)
);

CREATE INDEX idx_providers_name ON providers(name);

CREATE TABLE trainers (
  id            BIGSERIAL PRIMARY KEY,
  provider_id   BIGINT NULL REFERENCES providers(id) ON DELETE SET NULL,
  full_name     TEXT NOT NULL,
  email         TEXT NULL,
  phone         TEXT NULL,
  bio           TEXT NULL,
  certifications_json JSONB NULL,
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_trainers_provider_id ON trainers(provider_id);
CREATE INDEX idx_trainers_full_name ON trainers(full_name);

-- 4) Contracts and ledger
CREATE TABLE contracts (
  id                BIGSERIAL PRIMARY KEY,
  provider_id        BIGINT NOT NULL REFERENCES providers(id) ON DELETE RESTRICT,
  contract_number    TEXT NOT NULL,
  title              TEXT NULL,
  start_date         DATE NOT NULL,
  end_date           DATE NOT NULL,
  currency           TEXT NOT NULL DEFAULT 'KZT',
  budget_limit       NUMERIC(14,2) NOT NULL DEFAULT 0,
  status             TEXT NOT NULL DEFAULT 'draft',
  document_url       TEXT NULL,
  created_by_user_id BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT contracts_provider_number_uniq UNIQUE (provider_id, contract_number),
  CONSTRAINT contracts_status_chk CHECK (status IN ('draft', 'active', 'closed')),
  CONSTRAINT contracts_dates_chk CHECK (end_date >= start_date)
);

CREATE INDEX idx_contracts_provider_id ON contracts(provider_id);
CREATE INDEX idx_contracts_status ON contracts(status);
CREATE INDEX idx_contracts_dates ON contracts(start_date, end_date);

-- 5) Courses and sessions (schedule)
CREATE TABLE training_courses (
  id            BIGSERIAL PRIMARY KEY,
  provider_id   BIGINT NOT NULL REFERENCES providers(id) ON DELETE RESTRICT,
  title         TEXT NOT NULL,
  type          TEXT NOT NULL,
  description   TEXT NULL,
  default_duration_hours INT NULL,
  is_active     BOOLEAN NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT training_courses_type_chk CHECK (type IN ('seminar', 'training', 'certification'))
);

CREATE INDEX idx_training_courses_provider_id ON training_courses(provider_id);
CREATE INDEX idx_training_courses_title ON training_courses(title);

CREATE TABLE training_sessions (
  id            BIGSERIAL PRIMARY KEY,
  course_id     BIGINT NOT NULL REFERENCES training_courses(id) ON DELETE CASCADE,
  trainer_id    BIGINT NULL REFERENCES trainers(id) ON DELETE SET NULL,
  start_datetime TIMESTAMPTZ NOT NULL,
  end_datetime   TIMESTAMPTZ NOT NULL,
  city          TEXT NULL,
  location      TEXT NULL,
  capacity      INT NULL,
  price_model   TEXT NOT NULL DEFAULT 'per_person',
  price_amount  NUMERIC(14,2) NOT NULL DEFAULT 0,
  currency      TEXT NOT NULL DEFAULT 'KZT',
  status        TEXT NOT NULL DEFAULT 'scheduled',
  created_by_user_id BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT training_sessions_price_model_chk CHECK (price_model IN ('per_person', 'per_group')),
  CONSTRAINT training_sessions_status_chk CHECK (status IN ('scheduled', 'completed', 'cancelled')),
  CONSTRAINT training_sessions_dates_chk CHECK (end_datetime >= start_datetime)
);

CREATE INDEX idx_training_sessions_course_id ON training_sessions(course_id);
CREATE INDEX idx_training_sessions_trainer_id ON training_sessions(trainer_id);
CREATE INDEX idx_training_sessions_start ON training_sessions(start_datetime);
CREATE INDEX idx_training_sessions_status ON training_sessions(status);

-- 6) Applications (workflow)
CREATE TABLE applications (
  id                     BIGSERIAL PRIMARY KEY,
  requested_by_user_id    BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  requested_by_employee_id BIGINT NULL REFERENCES employees(id) ON DELETE SET NULL,
  organization_id         BIGINT NOT NULL REFERENCES organizations(id) ON DELETE RESTRICT,
  org_unit_id             BIGINT NULL REFERENCES org_units(id) ON DELETE SET NULL,
  course_id               BIGINT NOT NULL REFERENCES training_courses(id) ON DELETE RESTRICT,
  preferred_session_id    BIGINT NULL REFERENCES training_sessions(id) ON DELETE SET NULL,
  comment                 TEXT NULL,
  status                  TEXT NOT NULL DEFAULT 'draft',
  submitted_at            TIMESTAMPTZ NULL,
  hr_owner_user_id        BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
  decision_at             TIMESTAMPTZ NULL,
  decision_reason         TEXT NULL,
  linked_contract_id      BIGINT NULL REFERENCES contracts(id) ON DELETE SET NULL,
  created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT applications_status_chk CHECK (status IN (
    'draft', 'submitted', 'in_review', 'approved', 'rejected', 'cancelled'
  ))
);

CREATE INDEX idx_applications_requested_by ON applications(requested_by_user_id);
CREATE INDEX idx_applications_org ON applications(organization_id);
CREATE INDEX idx_applications_org_unit ON applications(org_unit_id);
CREATE INDEX idx_applications_status ON applications(status);
CREATE INDEX idx_applications_course ON applications(course_id);

CREATE TABLE application_items (
  id             BIGSERIAL PRIMARY KEY,
  application_id BIGINT NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  employee_id    BIGINT NOT NULL REFERENCES employees(id) ON DELETE RESTRICT,
  session_id     BIGINT NULL REFERENCES training_sessions(id) ON DELETE SET NULL,
  price_amount   NUMERIC(14,2) NOT NULL DEFAULT 0,
  currency       TEXT NOT NULL DEFAULT 'KZT',
  status         TEXT NOT NULL DEFAULT 'pending',
  created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT application_items_status_chk CHECK (status IN (
    'pending', 'approved', 'rejected', 'cancelled', 'enrolled', 'completed'
  )),
  CONSTRAINT application_items_uniq UNIQUE (application_id, employee_id)
);

CREATE INDEX idx_application_items_app_id ON application_items(application_id);
CREATE INDEX idx_application_items_employee_id ON application_items(employee_id);
CREATE INDEX idx_application_items_session_id ON application_items(session_id);
CREATE INDEX idx_application_items_status ON application_items(status);

CREATE TABLE application_status_history (
  id               BIGSERIAL PRIMARY KEY,
  application_id   BIGINT NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  from_status      TEXT NULL,
  to_status        TEXT NOT NULL,
  changed_by_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  comment          TEXT NULL,
  changed_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT app_status_history_to_chk CHECK (to_status IN (
    'draft', 'submitted', 'in_review', 'approved', 'rejected', 'cancelled'
  ))
);

CREATE INDEX idx_app_status_history_app_id ON application_status_history(application_id);
CREATE INDEX idx_app_status_history_changed_at ON application_status_history(changed_at);

-- Contract ledger references applications and items and sessions
CREATE TABLE contract_ledger (
  id                 BIGSERIAL PRIMARY KEY,
  contract_id         BIGINT NOT NULL REFERENCES contracts(id) ON DELETE CASCADE,
  entry_type          TEXT NOT NULL,
  amount              NUMERIC(14,2) NOT NULL,
  direction           TEXT NOT NULL,
  application_id      BIGINT NULL REFERENCES applications(id) ON DELETE SET NULL,
  application_item_id BIGINT NULL REFERENCES application_items(id) ON DELETE SET NULL,
  training_session_id BIGINT NULL REFERENCES training_sessions(id) ON DELETE SET NULL,
  comment             TEXT NULL,
  created_by_user_id  BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT contract_ledger_amount_chk CHECK (amount > 0),
  CONSTRAINT contract_ledger_direction_chk CHECK (direction IN ('debit', 'credit')),
  CONSTRAINT contract_ledger_entry_type_chk CHECK (entry_type IN ('reserve', 'writeoff', 'refund', 'adjustment'))
);

CREATE INDEX idx_contract_ledger_contract_id ON contract_ledger(contract_id);
CREATE INDEX idx_contract_ledger_application_id ON contract_ledger(application_id);
CREATE INDEX idx_contract_ledger_item_id ON contract_ledger(application_item_id);
CREATE INDEX idx_contract_ledger_session_id ON contract_ledger(training_session_id);
CREATE INDEX idx_contract_ledger_created_at ON contract_ledger(created_at);

-- 7) Participation / attendance / certificates
CREATE TABLE training_participants (
  id                   BIGSERIAL PRIMARY KEY,
  session_id            BIGINT NOT NULL REFERENCES training_sessions(id) ON DELETE CASCADE,
  employee_id           BIGINT NOT NULL REFERENCES employees(id) ON DELETE RESTRICT,
  application_item_id   BIGINT NULL REFERENCES application_items(id) ON DELETE SET NULL,
  enrolled_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  attendance_status     TEXT NOT NULL DEFAULT 'unknown',
  attendance_marked_by_user_id BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
  attendance_marked_at  TIMESTAMPTZ NULL,
  result_status         TEXT NOT NULL DEFAULT 'in_progress',
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT training_participants_attendance_chk CHECK (attendance_status IN ('unknown', 'present', 'absent')),
  CONSTRAINT training_participants_result_chk CHECK (result_status IN ('in_progress', 'completed', 'failed')),
  CONSTRAINT training_participants_uniq UNIQUE (session_id, employee_id)
);

CREATE INDEX idx_training_participants_session_id ON training_participants(session_id);
CREATE INDEX idx_training_participants_employee_id ON training_participants(employee_id);
CREATE INDEX idx_training_participants_attendance ON training_participants(attendance_status);

CREATE TABLE certificates (
  id                 BIGSERIAL PRIMARY KEY,
  participant_id     BIGINT NOT NULL REFERENCES training_participants(id) ON DELETE CASCADE,
  certificate_number TEXT NULL,
  issued_date        DATE NULL,
  file_url           TEXT NULL,
  issuer             TEXT NULL,
  created_by_user_id BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_certificates_participant_id ON certificates(participant_id);
CREATE INDEX idx_certificates_issued_date ON certificates(issued_date);

-- 8) Files (optional but useful) + polymorphic links
CREATE TABLE files (
  id                 BIGSERIAL PRIMARY KEY,
  storage_provider   TEXT NOT NULL DEFAULT 's3',
  url                TEXT NOT NULL,
  original_name      TEXT NULL,
  mime_type          TEXT NULL,
  size_bytes         BIGINT NULL,
  checksum           TEXT NULL,
  uploaded_by_user_id BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_files_created_at ON files(created_at);

CREATE TABLE file_links (
  id          BIGSERIAL PRIMARY KEY,
  file_id     BIGINT NOT NULL REFERENCES files(id) ON DELETE CASCADE,
  entity_type TEXT NOT NULL,
  entity_id   BIGINT NOT NULL,
  kind        TEXT NULL,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT file_links_entity_type_chk CHECK (entity_type IN (
    'contract', 'certificate', 'training_session', 'application'
  ))
);

CREATE INDEX idx_file_links_file_id ON file_links(file_id);
CREATE INDEX idx_file_links_entity ON file_links(entity_type, entity_id);

-- 9) Notifications (optional)
CREATE TABLE notifications (
  id          BIGSERIAL PRIMARY KEY,
  user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type        TEXT NOT NULL,
  payload_json JSONB NULL,
  is_read     BOOLEAN NOT NULL DEFAULT FALSE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  read_at     TIMESTAMPTZ NULL
);

CREATE INDEX idx_notifications_user_unread ON notifications(user_id, is_read, created_at);

COMMIT;