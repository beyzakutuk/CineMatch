import pandas as pd
import asyncio
import numpy as np
from datetime import datetime
from sqlalchemy import select
from db.database import engine, async_session
from db.model import Base, Title


def clean_value(val):
    if pd.isna(val) or (isinstance(val, float) and np.isnan(val)):
        return None
    if isinstance(val, str):
        return val.strip()
    return val

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%B %d, %Y").date()
    except:
        return None


async def import_data():
    print("combined_titles.csv dosyası yükleniyor...")
    df = pd.read_csv("data/combined_titles.csv")
    df.dropna(subset=["title", "platform"], inplace=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        count = 0
        for _, row in df.iterrows():
            title_name = clean_value(row.get("title"))
            platform = clean_value(row.get("platform"))

            if not title_name or not platform:
                continue  # zorunlu alanlar boşsa atla

            stmt = select(Title).where(
                Title.name == title_name,
                Title.platform == platform
            )
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                continue
            
            release_year_raw = clean_value(row.get("release_year"))
            release_year = int(release_year_raw) if release_year_raw is not None else None

            title = Title(
                show_id=clean_value(row.get("show_id")),
                name=title_name,
                type=clean_value(row.get("type")),
                director=clean_value(row.get("director")),
                cast=clean_value(row.get("cast")),
                country=clean_value(row.get("country")),
                date_added=parse_date(clean_value(row.get("date_added"))) if clean_value(row.get("date_added")) else None,
                release_year=release_year,
                rating=clean_value(row.get("rating")),
                duration=clean_value(row.get("duration")),
                listed_in=clean_value(row.get("listed_in")),
                description=clean_value(row.get("description")),
                platform=platform
            )
            count += 1
            session.add(title)
        await session.commit()
        print(f"✅ {count} içerik veritabanına eklendi.")

if __name__ == "__main__":
    asyncio.run(import_data())
