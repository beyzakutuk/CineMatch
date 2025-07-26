# api/main.py
from fastapi import FastAPI, Query
from db.model import Base
from db.database import engine
from api.endpoints import router as endpoints_router
from api.auth import router as auth_router
from recommender.content_based import ContentBasedRecommender

app = FastAPI(
    title="CineMatch - Content-Based Recommender",
    description="Film/dizi başlığına göre benzer içerikleri öneren API",
    version="1.0"
)

@app.on_event("startup")
async def on_startup():
    print("⏳ Veritabanı tabloları oluşturuluyor...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Veritabanı hazır.")

    # Global olarak recommender başlat
    global recommender
    recommender = ContentBasedRecommender()
    print("İçerik tabanlı önerici başlatıldı.")

@app.get("/recommendations/content/")
def recommend(
    title: str = Query(..., description="Öneri alınacak başlık"),
    n: int = Query(5, description="Kaç adet öneri gösterilecek")
):
    results = recommender.recommend_by_title(title, n)
    if not results:
        return {"message": f"Eşleşen içerik bulunamadı: {title}"}
    return results

# Diğer API endpointlerini dahil et
app.include_router(endpoints_router, prefix="/api")
app.include_router(auth_router, prefix="/auth")
