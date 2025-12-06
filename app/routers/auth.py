from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.security import create_access_token, hash_password, verify_password
from app.database import get_db
from app.models import User
from app.schemas.auth import LoginRequest, RegisterRequest

router = APIRouter(prefix="/auth", tags=["Auth"])


# @router.post("/register")
# async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
#     # Проверка пользователя
#     stmt = select(User).where(User.email == data.email)
#     existing = (await db.execute(stmt)).scalar_one_or_none()
#     if existing:
#         raise HTTPException(400, "Email already exists")

#     user = User(
#         email=data.email, hashed_password=hash_password(data.password), role="user"
#     )
#     db.add(user)
#     await db.commit()

#     return {"message": "User created"}


@router.post("/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    # form_data.username – это email
    user_query = (
        select(User)
        .where(User.email == form_data.username)
        .options(selectinload(User.role))
    )
    result = await db.execute(user_query)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Access Denied")

    token = create_access_token({"sub": str(user.id), "role": str(user.role.id)})
    return {"access_token": token, "token_type": "bearer"}