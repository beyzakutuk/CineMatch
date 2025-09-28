#schemas/title_schema.py
from pydantic import BaseModel
from typing import Optional

class TitleOut(BaseModel):
    id: int
    name: str
    listed_in: str #genre
    type: str 
    description: Optional[str]
    
    class Config: 
        orm_mode = True
