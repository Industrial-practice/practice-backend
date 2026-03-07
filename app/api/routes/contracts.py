from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_scoped_contract, is_hr
from app.db.session import get_db
from app.models.contract import Contract
from app.models.user import User
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
    current_user: User = Depends(get_current_user),
):
    if not is_hr(current_user):
        raise HTTPException(status_code=403, detail="Forbidden")

    return contract_service.get_all_contracts(db)


@router.get("/{contract_id}", response_model=ContractRead)
def get_contract(
    current_user: User = Depends(get_current_user),
    target_contract: Contract = Depends(get_scoped_contract),
):
    if not is_hr(current_user):
        raise HTTPException(status_code=403, detail="Forbidden")

    return target_contract


@router.post("/", response_model=ContractRead)
def create_contract(
    contract: ContractCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not is_hr(current_user):
        raise HTTPException(status_code=403, detail="Forbidden")

    return contract_service.create_contract(db, contract)


@router.put("/{contract_id}", response_model=ContractRead)
def update_contract(
    contract_id: int,
    contract: ContractUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    target_contract: Contract = Depends(get_scoped_contract),
):
    if not is_hr(current_user):
        raise HTTPException(status_code=403, detail="Forbidden")

    return contract_service.update_contract(db, contract_id, contract)


@router.delete("/{contract_id}")
def delete_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    target_contract: Contract = Depends(get_scoped_contract),
):
    if not is_hr(current_user):
        raise HTTPException(status_code=403, detail="Forbidden")

    return contract_service.delete_contract(db, contract_id)