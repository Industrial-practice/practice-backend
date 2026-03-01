from sqlalchemy.orm import Session
from app.models.contract import Contract


def get_contracts(db: Session):
    return db.query(Contract).all()


def get_contract(db: Session, contract_id: int):
    return db.query(Contract).filter(Contract.id == contract_id).first()


def create_contract(db: Session, contract: Contract):
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


def delete_contract(db: Session, contract: Contract):
    db.delete(contract)
    db.commit()