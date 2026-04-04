from fastapi import FastAPI, Request
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.database import engine, Base
from app.routers import auth, categories, expenses, budgets

security = HTTPBearer()

app = FastAPI(
    title="FinTrack API",
    description="REST API untuk manajemen keuangan pribadi",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

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