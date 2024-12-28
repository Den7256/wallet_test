from sqlalchemy.orm import Session
from models import Wallet
from schemas import WalletCreate

def get_wallet(db: Session, uuid: str):
    return db.query(Wallet).filter(Wallet.uuid == uuid).first()

def create_wallet(db: Session, wallet: WalletCreate):
    db_wallet = Wallet(uuid=wallet.uuid, balance=0)
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

def update_wallet_balance(db: Session, uuid: str, amount: float):
    wallet = get_wallet(db, uuid)
    if wallet:
        wallet.balance += amount
        db.commit()
        db.refresh(wallet)
        return wallet
    return None