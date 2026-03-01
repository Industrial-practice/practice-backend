from fastapi import Depends, HTTPException, Request
import jwt
import os
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )

        if payload["type"] != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user = db.query(User).filter(User.id == int(payload["sub"])).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(required_role: str):
    def role_checker(current_user=Depends(get_current_user)):
        token_role = current_user["role"]

        if token_role != required_role:
            raise HTTPException(status_code=403, detail="Forbidden")

        return current_user

    return role_checker