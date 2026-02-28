from sqlalchemy.orm import Session
from app.models.employee import Employee


def get_employees(db: Session):
    return db.query(Employee).all()


def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()


def create_employee(db: Session, employee: Employee):
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(db: Session, employee: Employee):
    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, employee: Employee):
    db.delete(employee)
    db.commit()