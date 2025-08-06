# api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from db.model import User, Title, Favorite
from db.database import get_db
from auth.dependencies import get_current_user

router = APIRouter()

@router.get("/titles/")
async def list_titles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Title))
    titles = result.scalars().all()
    return [{"id": t.id, "name": t.name} for t in titles]

@router.post("/favorites/")
async def add_favorite(title_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    fav = Favorite(user_id=current_user.id, title_id=title_id)
    db.add(fav)
    try:
        await db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Bu film/dizi favorilerde bulunuyor.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Favoriye eklendi"}

@router.get("/favorites/")
async def get_user_favorites(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Favorite).options(joinedload(Favorite.title)).where(Favorite.user_id == current_user.id)
    )
    
    favorites = result.scalars().all()
    return [{"title_id": fav.title_id, "title_name": fav.title.name} for fav in favorites]
