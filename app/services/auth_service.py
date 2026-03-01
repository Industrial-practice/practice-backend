from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.core.config import settings
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token
import jwt
import os


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive account")

    return user


def login(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    # Decode to extract jti + exp
    decoded = jwt.decode(
        refresh_token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
)

    refresh_record = RefreshToken(
        user_id=user.id,
        jti=decoded["jti"],
        expires_at=datetime.fromtimestamp(decoded["exp"], tz=timezone.utc),
    )

    db.add(refresh_record)
    db.commit()

    return access_token, refresh_token


def logout(db: Session, refresh_jti: str):
    token = db.query(RefreshToken).filter(
        RefreshToken.jti == refresh_jti
    ).first()

    if token:
        token.is_revoked = True
        db.commit()

def refresh_tokens(db: Session, refresh_token_str: str):
    if not refresh_token_str:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = jwt.decode(
            refresh_token_str,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    jti = payload.get("jti")
    user_id = int(payload.get("sub"))

    token_record = (
        db.query(RefreshToken)
        .filter(RefreshToken.jti == jti)
        .first()
    )

    if not token_record:
        raise HTTPException(status_code=401, detail="Token reuse detected")

    if token_record.is_revoked:
        raise HTTPException(status_code=401, detail="Token revoked")

    if token_record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Token expired")


    # Revoke old token
    token_record.is_revoked = True

    # Create new tokens
    user = token_record.user
    new_access = create_access_token(user)
    new_refresh = create_refresh_token(user)

    # Decode new refresh to store
    decoded_new = jwt.decode(
        new_refresh,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
    )

    new_record = RefreshToken(
        user_id=user_id,
        jti=decoded_new["jti"],
        expires_at=datetime.fromtimestamp(
            decoded_new["exp"], tz=timezone.utc
        ),
    )

    db.add(new_record)
    db.commit()

    return new_access, new_refresh

def revoke_refresh_token(db: Session, refresh_token_str: str):
    if not refresh_token_str:
        return

    try:
        payload = jwt.decode(
            refresh_token_str,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.InvalidTokenError:
        return

    jti = payload.get("jti")

    token = db.query(RefreshToken).filter(
        RefreshToken.jti == jti
    ).first()

    if token:
        token.is_revoked = True
        db.commit()