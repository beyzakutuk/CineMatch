# api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.model import User, Title, Favorite
from db.database import get_db

router = APIRouter()

from sqlalchemy.exc import IntegrityError

@router.post("/users/")
async def create_user(username: str, db: AsyncSession = Depends(get_db)):
    new_user = User(username=username)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten var.")
    return {"message": "Kullanıcı oluşturuldu", "user_id": new_user.id}

@router.get("/titles/")
async def list_titles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Title))
    titles = result.scalars().all()
    return [{"id": t.id, "name": t.name} for t in titles]

@router.post("/favorites/")
async def add_favorite(user_id: int, title_id: int, db: AsyncSession = Depends(get_db)):
    fav = Favorite(user_id=user_id, title_id=title_id)
    db.add(fav)
    try:
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Favoriye eklendi"}

@router.get("/favorites/{user_id}")
async def get_user_favorites(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Favorite).where(Favorite.user_id == user_id))
    favorites = result.scalars().all()
    return [{"title_id": fav.title_id} for fav in favorites]
