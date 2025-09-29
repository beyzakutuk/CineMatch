# api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from db.model import User, Title, Favorite
from db.database import get_db
from auth.dependencies import get_current_user
from schemas.title_schema import TitlesResponse

from recommender import recommender

router = APIRouter()

@router.get("/titles/", response_model=TitlesResponse)
async def list_titles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Title))
    titles = result.scalars().all()
    total = len(titles)
    return {"total": total, "titles": titles}

@router.get("/titles/search/", response_model=TitlesResponse)
async def search_titles( 
    q: str = Query(..., min_length=1, description="Aranacak içerik"), db: AsyncSession = Depends(get_db)):
    stmt = select(Title).where(
        or_(
            Title.name.ilike(f"%{q}%"),
            Title.director.ilike(f"%{q}%"),
            Title.cast.ilike(f"%{q}%"),
            Title.description.ilike(f"%{q}%"),
            Title.listed_in.ilike(f"%{q}%")
        )
        # genişletilebilir
    )
    
    result = await db.execute(stmt)
    titles = result.scalars().all()
    total = len(titles)
    return {"total": total, "titles": titles}

@router.get("/recommendations/favorites/")
async def recommend_by_favorites( n: int = Query(5, description="gösterilecek içerik sayısı"), db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Title.name).join(Favorite, Favorite.title_id == Title.id).where(Favorite.user_id == current_user.id)
    )
    
    favorite_titles = [row[0] for row in result.all()]
    if not favorite_titles:
        return {"message": "favorilenen içerik bulunamadı"}
    
    recommendations = recommender.recommend_by_user_favorites(favorite_titles, n)
    
    return{
        "based_on_favorites": favorite_titles,
        "recommendations": recommendations
    }

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

@router.delete("/favorites/")
async def remove_favorite(title_id: int, db: AsyncSession=Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Favorite).where(Favorite.user_id == current_user.id, Favorite.title_id == title_id)
    )
    
    favorite = result.scalar_one_or_none()
    
    if not favorite:
        raise HTTPException(status_code=404, detail="Favori Bulunamadı.")
    
    await db.delete(favorite)
    await db.commit()
    return {"message": "Favori Silindi."}

