from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session
import secrets

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas import UserRead, UserCreate
from app.schemas.auth import LoginRequest, AuthResponse
from app.services import auth_service, user_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserRead)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return user_service.create_user(db, user)

@router.post("/login", response_model=AuthResponse)
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    access_token, refresh_token = auth_service.login(
        db, data.email, data.password
    )
    csrf_token = secrets.token_urlsafe(32)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        secure=True,
        samesite="strict",
    )

    response.headers["X-CSRF-Token"] = csrf_token

    return {"message": "Login successful", "csrf_token": csrf_token}

@router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")

    access, refresh_new = auth_service.refresh_tokens(
        db, refresh_token
    )
    csrf_token = secrets.token_urlsafe(32)

    response.set_cookie(
        key="access_token",
        value=access,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_new,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        secure=True,
        samesite="strict",
    )

    response.headers["X-CSRF-Token"] = csrf_token

    return {"message": "Token refreshed", "csrf_token": csrf_token}

@router.get("/me", response_model=UserRead)
def get_me(current_user = Depends(get_current_user)):
    return current_user

@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")

    auth_service.revoke_refresh_token(db, refresh_token)

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("csrf_token")

    return {"message": "Logged out"}