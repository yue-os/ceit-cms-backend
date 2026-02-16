from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.services import auth_service
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)) -> Token:
    return await auth_service.authenticate_user(db=db, email=email, password=password)