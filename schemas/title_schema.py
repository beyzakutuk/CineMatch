#schemas/title_schema.py
from pydantic import BaseModel
from typing import Optional, List

class TitleOut(BaseModel):
    id: int
    name: str
    listed_in: str #genre
    type: str 
    description: Optional[str]
    
class Config: 
    orm_mode = True
    
class TitlesResponse(BaseModel):
    total: int
    titles: List[TitleOut]

