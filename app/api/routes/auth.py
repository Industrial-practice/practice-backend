from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas import UserRead, UserCreate
from app.schemas.auth import LoginRequest, AuthResponse
from app.services import auth_service, user_service
from fastapi import HTTPException
import jwt
import os

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

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
    )

    return {"message": "Login successful"}

@router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")

    access, refresh_new = auth_service.refresh_tokens(
        db, refresh_token
    )

    response.set_cookie(
        key="access_token",
        value=access,
        httponly=True,
        secure=True,
        samesite="none",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_new,
        httponly=True,
        secure=True,
        samesite="none",
    )

    return {"message": "Token refreshed"}

@router.get("/me", response_model=UserRead)
def get_me(current_user = Depends(get_current_user)):
    return current_user

@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")

    auth_service.revoke_refresh_token(db, refresh_token)

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"message": "Logged out"}