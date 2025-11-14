from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import User
from app.schemas.users import UserCreate, UserRead

router = APIRouter(prefix="/users")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@router.get("/", response_model=list[UserRead])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).options(selectinload(User.role)))
    return result.scalars().all()

@router.post("/", response_model=UserRead)
async def add_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    
    new_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password),
        role_id=user.role_id,
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    user = await db.execute(
        select(User).options(selectinload(User.role)).where(User.id == new_user.id)
    )
    result = user.scalar_one_or_none()
    return result