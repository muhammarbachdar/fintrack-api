from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import AsyncSessionLocal
from app.core.security import decode_token
from app.models.budget import Budget
from app.models.expense import Expense, TransactionType
from app.schemas.budget import BudgetCreate, BudgetResponse
from fastapi.security import OAuth2PasswordBearer
from typing import List

router = APIRouter(prefix="/budgets", tags=["budgets"])
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

@router.post("/", response_model=BudgetResponse)
async def create_budget(
    data: BudgetCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    budget = Budget(**data.model_dump(), user_id=user_id)
    db.add(budget)
    await db.commit()
    await db.refresh(budget)
    return budget

@router.get("/", response_model=List[BudgetResponse])
async def get_budgets(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Budget).where(Budget.user_id == user_id))
    return result.scalars().all()

@router.get("/report/{month}")
async def get_report(
    month: str,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Total income
    income = await db.execute(
        select(func.sum(Expense.amount)).where(
            Expense.user_id == user_id,
            Expense.type == TransactionType.income
        )
    )
    total_income = income.scalar() or 0

    # Total expense
    expense = await db.execute(
        select(func.sum(Expense.amount)).where(
            Expense.user_id == user_id,
            Expense.type == TransactionType.expense
        )
    )
    total_expense = expense.scalar() or 0

    return {
        "month": month,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }