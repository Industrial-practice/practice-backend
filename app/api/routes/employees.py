from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_current_org_unit_id,
    get_current_user,
    get_scoped_employee,
    is_employee,
    is_head,
    is_hr,
)
from app.db.session import get_db
from app.models.employee import Employee
from app.models.user import User
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeRead,
    EmployeeUpdate
)
from app.services import employee_service

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[EmployeeRead])
def get_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if is_hr(current_user):
        return employee_service.get_all_employees(db)

    if is_head(current_user):
        current_org_unit_id = get_current_org_unit_id(current_user)
        if current_org_unit_id is None:
            return []
        return (
            db.query(Employee)
            .filter(Employee.org_unit_id == current_org_unit_id)
            .all()
        )

    if is_employee(current_user):
        if current_user.employee:
            return [current_user.employee]
        return []

    return []


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(target_employee: Employee = Depends(get_scoped_employee)):
    return target_employee


@router.post("/", response_model=EmployeeRead)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not is_hr(current_user):
        raise HTTPException(status_code=403, detail="Forbidden")

    return employee_service.create_employee(db, employee)


@router.put("/{employee_id}", response_model=EmployeeRead)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    target_employee: Employee = Depends(get_scoped_employee),
):
    if not is_hr(current_user):
        raise HTTPException(status_code=403, detail="Forbidden")

    return employee_service.update_employee(db, employee_id, employee)


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not is_hr(current_user):
        raise HTTPException(status_code=403, detail="Forbidden")

    return employee_service.delete_employee(db, employee_id)