# api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from auth.utils import hash_password, create_access_token, verify_password
from db.model import User
from db.database import get_db
from schemas.auth_schema import RegisterRequest, LoginRequest,TokenResponce

router = APIRouter()
    
@router.post("/register", response_model=TokenResponce)
async def register_user(user_data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(
        select(User).where(
            (User.email == user_data.email) |  (User.username == user_data.username)
        )
    )
    
    user_in_db = existing_user.scalars().first()
    if user_in_db:
        raise HTTPException(status_code=400, detail="Bu kullanıcı veri tabanında mevcut")
    
    hashed_password = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        username = user_data.username,
        password = hashed_password
    )
    
    db.add(user)
    
    try:
        await db.commit()
        await db.refresh(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hata Oluştu: {str(e)}")
    
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponce)
async def login_user(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == login_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Girilen kullanıcı bilgileri geçersiz.")
    
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
    