# 🔐 RBAC Model (Role-Based Access Control)

**Practice Project:** Offline Training Management  
**Written by:** Security  
**Version:** 1.1  

---

# 1. Purpose

This document defines the Role-Based Access Control (RBAC) model for the system.

The goal is to:

- Enforce least privilege principle
- Prevent unauthorized data access
- Protect sensitive business and personal data
- Prevent IDOR (Insecure Direct Object Reference) vulnerabilities

This document is normative for backend authorization behavior.

---

# 2. Roles Overview

The system defines three primary roles:

- **HR (Admin)**
- **Head of Department**
- **Employee**

Access is determined by:
- User role
- Department ownership
- Object-level validation (resource ownership)

Default rule: any action not explicitly allowed is denied.

---

# 3. Role Definitions

## 3.1 HR (Admin)

Full administrative control over training processes.

Permissions:

- Create, edit, and delete contracts
- Create and manage training events
- Approve or reject training requests
- Assign requests to contracts (budget spending)
- Mark attendance
- Upload certificates
- View all employees and all departments
- View budget consumption

Restrictions:

- Cannot bypass audit logging
- Cannot access system-level secrets

---

## 3.2 Head of Department

Manages employees within their department.

Permissions:

- View training catalog (read-only)
- Submit training requests for employees in their department
- View request status
- View training results of employees in their department
- View certificates of employees in their department

Restrictions:

- Cannot create or modify contracts
- Cannot approve or reject requests
- Cannot access other departments' data
- Cannot modify attendance or certificates

---

## 3.3 Employee

Limited personal access only.

Permissions:

- View own assigned training
- View own request status
- View own attendance records
- View own certificates

Restrictions:

- Cannot submit requests
- Cannot modify any training data
- Cannot view other employees' data
- Cannot access contracts or budgets

---

# 4. Access Matrix

| Action                  | HR | Head of Department |    Employee   |
|-------------------------|----|--------------------|---------------|
| Create Contract         | ✅ | ❌                | ❌            |
| Edit Contract           | ✅ | ❌                | ❌            |
| View Contract           | ✅ | ❌                | ❌            |
| Create Training         | ✅ | ❌                | ❌            |
| Submit Training Request | ❌ | ✅                | ❌            |
| Approve Request         | ✅ | ❌                | ❌            |
| View Request Status     | ✅ | ✅ (own dept)     | ✅ (own only) |
| Mark Attendance         | ✅ | ❌                | ❌            |
| Upload Certificate      | ✅ | ❌                | ❌            |
| View Certificate        | ✅ | ✅ (own dept)     | ✅ (own only) |
| View Budget Consumption | ✅ | ❌                | ❌            |

Matrix interpretation rules:
- `✅` means role-level access is allowed, still subject to object-level checks.
- `✅ (own dept)` requires department match against `current_user.department_id`.
- `✅ (own only)` requires ownership match against `current_user.id`.
- Any unlisted action is denied.

---

# 5. Object-Level Security Rules

In addition to role checks, object-level validation is mandatory.

## 5.1 Department-Based Access

Head of Department may only access:
- Employees within their department
- Requests submitted for their department
- Certificates belonging to their department

Validation rule example:

- `employee.department_id == current_user.department_id`
- with precondition: `current_user.role == "head_of_department"`

---

## 5.2 Ownership Validation

Employees may only access:
- Resources where `resource.user_id == current_user.id`

Recommended reusable checks:
- `is_same_department(resource_department_id, current_user.department_id)`
- `is_owner(resource_user_id, current_user.id)`

---

# 6. IDOR Protection

All endpoints accessing resources by ID must:

1. Validate JWT
2. Validate user role
3. Validate department ownership or resource ownership



Must verify:
- HR → allowed
- Head of Department → only if employee.department_id matches
- Employee → only if employee.id == current_user.id

Failure to validate leads to IDOR vulnerability.

For list endpoints, apply ownership/department filters at query level (not only after fetch).

---

# 7. Authorization Enforcement Strategy

RBAC must be enforced at backend level using:

- Dependency-based role validation
- Object-level access checks
- Centralized authorization middleware

Authorization must NOT rely on frontend logic.

Recommended backend order:
1. Authenticate (`401` on failure)
2. Authorize role (`403` on failure)
3. Authorize object scope (`403` on failure)

---

# 8. Security Principles

This RBAC model follows:

- Principle of Least Privilege
- Need-to-Know access
- Separation of Duties
- Defense-in-Depth
- Default Deny

Authorization decisions:
- Explicit allow + object-level pass → permit
- Any other case → deny

---

# 9. Error Handling

- 401 Unauthorized → invalid or missing token
- 403 Forbidden → valid token but insufficient permissions

Do not expose internal authorization logic in error messages.

Use consistent response bodies for denied access to reduce information leakage.

---

# 10. Audit Requirements

The following actions must be logged:

- Request approval/rejection
- Contract modifications
- Budget assignments
- Certificate uploads
- Attendance marking

Audit logs must include:
- User ID
- Role
- Timestamp
- Action performed
- Resource affected

Additional requirements:
- Log authorization failures for sensitive endpoints
- Keep audit logs immutable and access-restricted
- Define retention period according to internal policy
