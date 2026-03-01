from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeRead,
    EmployeeUpdate
)
from app.services import employee_service

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", response_model=list[EmployeeRead])
def get_employees(db: Session = Depends(get_db)):
    return employee_service.get_all_employees(db)


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    return employee_service.get_employee_by_id(db, employee_id)


@router.post("/", response_model=EmployeeRead)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    return employee_service.create_employee(db, employee)


@router.put("/{employee_id}", response_model=EmployeeRead)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    return employee_service.update_employee(db, employee_id, employee)


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    return employee_service.delete_employee(db, employee_id)