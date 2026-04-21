from pydantic import BaseModel
from typing import Optional

class MenuBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    image_url: Optional[str] = None

class MenuCreate(MenuBase):
    restaurant_id: int

class MenuResponse(MenuBase):
    id: int
    restaurant_id: int

    class Config:
        from_attributes = True