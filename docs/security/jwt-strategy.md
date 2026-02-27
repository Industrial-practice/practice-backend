# 🔐 JWT Authentication Strategy

**Practice Project:** Offline Training Management  
**Written by:** Security  
**Version:** 1.1  

---

# 1. Purpose

This document defines the JWT authentication strategy for the system.

Objectives:
- Secure authentication
- Stateless session handling
- Role-based access control (RBAC)
- Protection against token misuse and theft
- Alignment with modern security best practices

---

# 2. Authentication Architecture

The system uses a dual-token model:
- **Access Token** (short-lived: 10-15 minutes) need to clarify with Director
- **Refresh Token** (long-lived: 7-14 days)

This model balances security and user experience.

---

# 3. Access Token

## 3.1 Purpose

Used to authorize requests to protected API endpoints.

## 3.2 Characteristics

- Lifetime: 15 minutes
- Algorithm: HS256
- Required for all protected endpoints
- Contains only minimal authorization claims

## 3.3 Payload Structure

```json
{
  "sub": "123",
  "role": "head_of_department",
  "department_id": 5,
  "type": "access",
  "iat": 1712340000,
  "exp": 1712340900,
  "jti": "3e6f4d4e-38ea-4b06-9bb2-1aa45fcb9b4d"
}
```

## 3.4 Security Requirements

The Access Token:
- Must NOT contain personal data (name, email, certificates, etc.)
- Must NOT contain sensitive business data
- Must include `exp` and be validated on every request
- Must include `type = "access"`
- Must be rejected if malformed, expired, or signature-invalid

---

# 4. Refresh Token

## 4.1 Purpose

Used only to issue a new Access Token without requiring re-login.

## 4.2 Characteristics

- Lifetime: 7-14 days
- Scope: `/refresh` endpoint only
- Cannot access protected resources directly
- Should be rotated on every successful refresh

## 4.3 Payload Structure

```json
{
  "sub": "123",
  "type": "refresh",
  "iat": 1712340000,
  "exp": 1719999999,
  "jti": "9cc3c7f3-2b84-44a7-9a1b-d8395a6f7aa4"
}
```

## 4.4 Security Requirements

The Refresh Token:
- Must contain minimal claims (`sub`, `type`, `iat`, `exp`, `jti`)
- Must NOT include role or authorization claims
- Must NOT be accepted as an access token
- Must be validated against server-side token state (allowlist/denylist)

---

# 5. Token Storage Policy

Tokens are stored in secure cookies:
- `HttpOnly=true`
- `Secure=true` (HTTPS only)
- `SameSite=Strict` (or `Lax` if cross-domain flow is required)

Tokens must NOT be stored in:
- `localStorage`
- `sessionStorage`

Additional controls:
- Use a CSRF protection strategy for cookie-authenticated state-changing requests
- Clear auth cookies explicitly on logout

---

# 6. Signing and Secret Management

- Algorithm: `HS256`
- Secret must be read from environment variables
- Secret must never be committed to Git
- Use different secrets for development, staging, and production
- Rotate secrets periodically and after any suspected compromise

Example:

```env
JWT_SECRET=strong_random_secret_key
JWT_ALGORITHM=HS256
```

---

# 7. Authentication Flow

## 7.1 Login Flow

1. User submits credentials.
2. Password is verified with `bcrypt` since we started with it.
3. Server issues:
   - Access Token (15 minutes)
   - Refresh Token (7-14 days)
4. Tokens are set in HttpOnly secure cookies.

## 7.2 Accessing Protected Endpoints

Backend validates:
- Signature
- Expiration
- Token type (`access`)
- Required authorization claims (role/department where applicable)

Authorization evaluation order:
1. Authenticate token (`401` on failure)
2. Authorize role (`403` on failure)
3. Authorize object scope/ownership (`403` on failure)

Authorization policy:
- Explicit allow + object-level pass → permit
- Any other case → deny (default deny)

If valid: request proceeds.  
If invalid: return `401 Unauthorized`.

## 7.3 Refresh Flow

1. Client calls `/refresh` with refresh cookie.
2. Backend validates refresh token signature, expiration, and type.
3. Backend checks token state (`jti`) and rotation policy.
4. If valid: issue new access token and rotate refresh token.
5. If invalid/reused: revoke session and return `401 Unauthorized`.

---

# 8. Logout Strategy

On logout:
- Invalidate refresh token server-side (by `jti` or session record)
- Clear auth cookies
- Keep access token lifetime short so residual token risk is minimized

---

# 9. Error Handling and Status Codes

- `401 Unauthorized`: missing/invalid/expired token
- `403 Forbidden`: authenticated user lacks required role/permission

Avoid returning detailed token validation internals in responses.
Use consistent error response shapes to reduce information leakage.

---

# 10. Security Controls Checklist

- Short-lived access tokens
- Long-lived refresh tokens with rotation
- HttpOnly + Secure cookie storage
- Minimal token payload
- Signature and token-type verification
- RBAC enforcement at endpoint level
- Default-deny authorization behavior
- Rate limiting on login and refresh endpoints
- Audit logging for login, refresh, and logout events