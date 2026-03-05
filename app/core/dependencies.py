from fastapi import Depends, HTTPException, Request
import jwt
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

        if not user.is_active:
            raise HTTPException(status_code=403, detail="Inactive account")

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(*required_roles: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        user_roles = {user_role.role.code for user_role in current_user.user_roles}
        if not user_roles.intersection(set(required_roles)):
            raise HTTPException(status_code=403, detail="Forbidden")

        return current_user

    return role_checker