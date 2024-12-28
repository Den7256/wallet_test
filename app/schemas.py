from pydantic import BaseModel

class WalletCreate(BaseModel):
    uuid: str

class Operation(BaseModel):
    operationType: str
    amount: float