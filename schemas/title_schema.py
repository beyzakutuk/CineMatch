#schemas/title_schema.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class TitleOut(BaseModel):
    id: int
    name: str
    listed_in: str #genre
    type: str 
    description: Optional[str]
    
class TitlesResponse(BaseModel):
    total: int
    titles: List[TitleOut]

class TitleDetail(BaseModel):
    id: int
    name: str
    type: Optional[str]
    director: Optional[str]
    cast: Optional[str]
    country: Optional[str]
    date_added: Optional[date]
    release_year: Optional[int]
    rating: Optional[str]
    duration: Optional[str]
    listed_in: Optional[str]
    description: Optional[str]
    platform: Optional[str]
    
class Config: 
    orm_mode = True
    