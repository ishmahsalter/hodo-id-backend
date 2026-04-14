from pydantic import BaseModel, EmailStr
from typing import Optional, List

# ==================== USER SCHEMAS ====================

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True

# ==================== MENU SCHEMAS ====================

class MenuBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str  # Makanan atau Minuman
    image_url: Optional[str] = None

class MenuCreate(MenuBase):
    restaurant_id: int

class MenuResponse(MenuBase):
    id: int
    restaurant_id: int

    class Config:
        from_attributes = True

# ==================== RESTAURANT SCHEMAS ====================

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

# ==================== AUTH SCHEMAS ====================

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None