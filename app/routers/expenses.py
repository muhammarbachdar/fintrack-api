from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.core.security import decode_token
from app.models.expense import Expense, TransactionType
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional

router = APIRouter(prefix="/expenses", tags=["expenses"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        return int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Token tidak valid")

@router.post("/", response_model=ExpenseResponse)
async def create_expense(
    data: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    expense = Expense(**data.model_dump(), user_id=user_id)
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense

@router.get("/", response_model=List[ExpenseResponse])
async def get_expenses(
    category_id: Optional[int] = None,
    type: Optional[TransactionType] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    query = select(Expense).where(Expense.user_id == user_id)
    
    if category_id:
        query = query.where(Expense.category_id == category_id)
    if type:
        query = query.where(Expense.type == type)
    if start_date:
        query = query.where(Expense.date >= start_date)
    if end_date:
        query = query.where(Expense.date <= end_date)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.delete("/{expense_id}")
async def delete_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Expense).where(Expense.id == expense_id, Expense.user_id == user_id))
    expense = result.scalar_one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense tidak ditemukan")
    await db.delete(expense)
    await db.commit()
    return {"message": "Expense berhasil dihapus"}
@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: int,
    data: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Expense).where(Expense.id == expense_id, Expense.user_id == user_id))
    expense = result.scalar_one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense tidak ditemukan")
    
    for key, value in data.model_dump().items():
        setattr(expense, key, value)
    
    await db.commit()
    await db.refresh(expense)
    return expense