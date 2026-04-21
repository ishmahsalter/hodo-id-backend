from pydantic import BaseModel
from typing import Optional, List
from schemas.menu import MenuResponse

class RestaurantBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    phone: str
    image_url: Optional[str] = None

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantResponse(RestaurantBase):
    id: int
    owner_id: int
    menus: List[MenuResponse] = []

    class Config:
        from_attributes = True