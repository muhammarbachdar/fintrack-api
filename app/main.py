from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.core.database import engine, Base
from app.routers import auth, categories, expenses, budgets

security = HTTPBearer()

app = FastAPI()

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(expenses.router)
app.include_router(budgets.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health_check():
    return {"status": "online"}