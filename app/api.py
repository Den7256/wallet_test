from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from . import crud, schemas

router = APIRouter()


@router.post("/api/v1/wallets/{wallet_uuid}/operation")
def perform_operation(wallet_uuid: str, operation: schemas.Operation, db: Session = Depends(get_db)):
    wallet = crud.get_wallet(db, wallet_uuid)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if operation.operationType not in ["DEPOSIT", "WITHDRAW"]:
        raise HTTPException(status_code=400, detail="Invalid operation type")

    if operation.operationType == "WITHDRAW" and wallet.balance < operation.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Update balance
    amount = operation.amount if operation.operationType == "DEPOSIT" else -operation.amount
    updated_wallet = crud.update_wallet_balance(db, wallet_uuid, amount)

    return {"balance": updated_wallet.balance}


@router.get("/api/v1/wallets/{wallet_uuid}")
def read_wallet(wallet_uuid: str, db: Session = Depends(get_db)):
    wallet = crud.get_wallet(db, wallet_uuid)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {"balance": wallet.balance}