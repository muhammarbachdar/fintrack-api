from pydantic import BaseModel

class BudgetCreate(BaseModel):
    category_id: int
    amount: float
    month: str

class BudgetResponse(BaseModel):
    id: int
    category_id: int
    user_id: int
    amount: float
    month: str

    class Config:
        from_attributes = True