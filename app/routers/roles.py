from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Role
from app.schemas.roles import RoleCreate, RoleRead

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=list[RoleRead])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role))
    return result.scalars().all()

@router.post("/", response_model=RoleRead)
async def add_user(role: RoleCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Role).where(Role.name == role.name))
    existing_role = result.scalar_one_or_none()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This role already exists",
        )

    new_role = Role(
        name = role.name
    )

    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    role = await db.execute(
        select(Role).where(Role.id == new_role.id)
    )
    result = role.scalar_one_or_none()
    return result