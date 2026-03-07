from fastapi import Depends, HTTPException, Request
import jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.application import Application
from app.models.contract import Contract
from app.models.employee import Employee
from app.models.user import User


HR_ROLE_CODES = {"hr", "admin"}
HEAD_ROLE_CODES = {"head_of_department", "head"}
EMPLOYEE_ROLE_CODES = {"employee"}


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


def get_role_codes(current_user: User) -> set[str]:
    return {
        (user_role.role.code or "").lower().strip()
        for user_role in current_user.user_roles
        if user_role.role and user_role.role.code
    }


def is_hr(current_user: User) -> bool:
    return bool(get_role_codes(current_user).intersection(HR_ROLE_CODES))


def is_head(current_user: User) -> bool:
    return bool(get_role_codes(current_user).intersection(HEAD_ROLE_CODES))


def is_employee(current_user: User) -> bool:
    return bool(get_role_codes(current_user).intersection(EMPLOYEE_ROLE_CODES))


def get_current_employee(current_user: User) -> Employee | None:
    return current_user.employee


def get_current_org_unit_id(current_user: User) -> int | None:
    employee = get_current_employee(current_user)
    if not employee:
        return None
    return employee.org_unit_id


def get_current_organization_id(current_user: User) -> int | None:
    employee = get_current_employee(current_user)
    if not employee:
        return None
    return employee.organization_id


def get_scoped_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    if is_hr(current_user):
        return target_user

    if is_head(current_user):
        current_org_unit_id = get_current_org_unit_id(current_user)
        target_employee = target_user.employee
        if (
            current_org_unit_id is not None
            and target_employee
            and target_employee.org_unit_id == current_org_unit_id
        ):
            return target_user
        raise HTTPException(status_code=403, detail="Forbidden")

    if target_user.id == current_user.id:
        return target_user

    raise HTTPException(status_code=403, detail="Forbidden")


def get_scoped_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Employee:
    target_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not target_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if is_hr(current_user):
        return target_employee

    if is_head(current_user):
        current_org_unit_id = get_current_org_unit_id(current_user)
        if (
            current_org_unit_id is not None
            and target_employee.org_unit_id == current_org_unit_id
        ):
            return target_employee
        raise HTTPException(status_code=403, detail="Forbidden")

    current_employee = get_current_employee(current_user)
    if current_employee and current_employee.id == target_employee.id:
        return target_employee

    raise HTTPException(status_code=403, detail="Forbidden")


def get_scoped_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Application:
    target_application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )
    if not target_application:
        raise HTTPException(status_code=404, detail="Application not found")

    if is_hr(current_user):
        return target_application

    if is_head(current_user):
        current_org_unit_id = get_current_org_unit_id(current_user)
        if (
            current_org_unit_id is not None
            and target_application.org_unit_id == current_org_unit_id
        ):
            return target_application
        raise HTTPException(status_code=403, detail="Forbidden")

    if target_application.requested_by_user_id == current_user.id:
        return target_application

    raise HTTPException(status_code=403, detail="Forbidden")


def get_scoped_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Contract:
    target_contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not target_contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    if is_hr(current_user):
        return target_contract

    raise HTTPException(status_code=403, detail="Forbidden")