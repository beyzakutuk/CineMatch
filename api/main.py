# api/main.py
from fastapi import FastAPI, Query
from db.model import Base
from db.database import engine
from api.endpoints import router as endpoints_router
from api.auth import router as auth_router
from recommender.content_based import ContentBasedRecommender
from fastapi.openapi.utils import get_openapi
from data.import_titles import import_data

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

    await import_data() 
    
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

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="JWT auth with Swagger",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(endpoints_router, prefix="/api")
app.include_router(auth_router, prefix="/auth")
