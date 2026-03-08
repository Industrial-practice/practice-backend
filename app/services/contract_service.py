from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.contract import Contract
from app.schemas.contract import ContractCreate, ContractUpdate
from app.repositories import contract_repository, provider_repository


def get_all_contracts(db: Session, organization_id: int):

    return db.query(Contract).filter(
        Contract.organization_id == organization_id
    ).all()


def get_contract_by_id(
    db: Session,
    contract_id: int,
    organization_id: int
):

    contract = db.query(Contract).filter(
        Contract.id == contract_id,
        Contract.organization_id == organization_id
    ).first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    return contract


def create_contract(
    db: Session,
    organization_id: int,
    contract_data: ContractCreate,
    user_id: int
):

    provider = provider_repository.get_provider(
        db,
        contract_data.provider_id
    )

    if not provider:
        raise HTTPException(
            status_code=404,
            detail="Provider not found"
        )

    contract = Contract(
        **contract_data.model_dump(),
        organization_id=organization_id,
        created_by_user_id=user_id
    )

    return contract_repository.create_contract(db, contract)


def update_contract(
    db: Session,
    contract_id: int,
    organization_id: int,
    data: ContractUpdate
):

    contract = db.query(Contract).filter(
        Contract.id == contract_id,
        Contract.organization_id == organization_id
    ).first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(contract, key, value)

    return contract_repository.update_contract(db, contract)


def delete_contract(
    db: Session,
    contract_id: int,
    organization_id: int
):

    contract = db.query(Contract).filter(
        Contract.id == contract_id,
        Contract.organization_id == organization_id
    ).first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    contract_repository.delete_contract(db, contract)

    return {"message": "Contract deleted"}