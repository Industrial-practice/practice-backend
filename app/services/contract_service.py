from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.contract import Contract
from app.schemas.contract import ContractCreate, ContractUpdate
from app.repositories import contract_repository


def get_all_contracts(db: Session):
    return contract_repository.get_contracts(db)


def get_contract_by_id(db: Session, contract_id: int):
    contract = contract_repository.get_contract(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract


def create_contract(db: Session, contract_data: ContractCreate):
    contract = Contract(**contract_data.model_dump())
    return contract_repository.create_contract(db, contract)


def update_contract(db: Session, contract_id: int, data: ContractUpdate):
    contract = contract_repository.get_contract(db, contract_id)

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(contract, key, value)

    return contract_repository.update_contract(db, contract)


def delete_contract(db: Session, contract_id: int):
    contract = contract_repository.get_contract(db, contract_id)

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    contract_repository.delete_contract(db, contract)
    return {"message": "Contract deleted"}