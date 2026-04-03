from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.core.security import decode_token
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/categories", tags=["categories"])
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

@router.post("/", response_model=CategoryResponse)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    category = Category(name=data.name, user_id=user_id)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category

@router.get("/", response_model=list[CategoryResponse])
async def get_categories(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    result = await db.execute(select(Category).where(Category.user_id == user_id))
    return result.scalars().all()