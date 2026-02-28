from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.repositories import employee_repository


def get_all_employees(db: Session):
    return employee_repository.get_employees(db)


def get_employee_by_id(db: Session, employee_id: int):
    employee = employee_repository.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


def create_employee(db: Session, employee_data: EmployeeCreate):
    employee = Employee(**employee_data.model_dump())
    return employee_repository.create_employee(db, employee)


def update_employee(db: Session, employee_id: int, data: EmployeeUpdate):
    employee = employee_repository.get_employee(db, employee_id)

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)

    return employee_repository.update_employee(db, employee)


def delete_employee(db: Session, employee_id: int):
    employee = employee_repository.get_employee(db, employee_id)

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee_repository.delete_employee(db, employee)
    return {"message": "Employee deleted"}