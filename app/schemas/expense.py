from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.expense import TransactionType

class ExpenseCreate(BaseModel):
    amount: float
    description: Optional[str] = None
    type: TransactionType
    category_id: Optional[int] = None

class ExpenseResponse(BaseModel):
    id: int
    amount: float
    description: Optional[str] = None
    type: TransactionType
    category_id: Optional[int] = None
    user_id: int
    date: datetime

    class Config:
        from_attributes = True