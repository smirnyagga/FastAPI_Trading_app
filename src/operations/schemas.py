from datetime import datetime

from pydantic import BaseModel


class OperationRead(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str

    class Config:
        from_attributes = True


class OperationCreate(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str

    class Config:
        from_attributes = True
