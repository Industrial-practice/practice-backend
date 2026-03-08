from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.schemas.contract import (
    ContractCreate,
    ContractRead,
    ContractUpdate
)
from app.services import contract_service

router = APIRouter(
    prefix="/contracts",
    tags=["Contracts"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[ContractRead])
def get_contracts(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    organization_id = user.employee.organization_id

    return contract_service.get_all_contracts(
        db,
        organization_id
    )


@router.get("/{contract_id}", response_model=ContractRead)
def get_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    organization_id = user.employee.organization_id

    return contract_service.get_contract_by_id(
        db,
        contract_id,
        organization_id
    )


@router.post("/", response_model=ContractRead)
def create_contract(
    contract: ContractCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    organization_id = user.employee.organization_id

    return contract_service.create_contract(
        db,
        organization_id,
        contract,
        user.id
    )


@router.put("/{contract_id}", response_model=ContractRead)
def update_contract(
    contract_id: int,
    contract: ContractUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    organization_id = user.employee.organization_id

    return contract_service.update_contract(
        db,
        contract_id,
        organization_id,
        contract
    )


@router.delete("/{contract_id}")
def delete_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    organization_id = user.employee.organization_id

    return contract_service.delete_contract(
        db,
        contract_id,
        organization_id
    )