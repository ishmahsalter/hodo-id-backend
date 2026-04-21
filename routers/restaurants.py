from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.restaurant import Restaurant
from schemas.restaurant import RestaurantCreate, RestaurantResponse
from auth.security import get_current_active_user

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.get("/", response_model=List[RestaurantResponse])
def get_all_restaurants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    restaurants = db.query(Restaurant).offset(skip).limit(limit).all()
    return restaurants

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant_by_id(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restoran tidak ditemukan")
    return restaurant

@router.post("/", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
def create_restaurant(
    restaurant: RestaurantCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_restaurant = Restaurant(
        name=restaurant.name,
        description=restaurant.description,
        address=restaurant.address,
        phone=restaurant.phone,
        image_url=restaurant.image_url,
        owner_id=current_user.id
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(
    restaurant_id: int,
    restaurant_update: RestaurantCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restoran tidak ditemukan")
    
    if db_restaurant.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Anda bukan pemilik restoran ini")
    
    for key, value in restaurant_update.model_dump().items():
        setattr(db_restaurant, key, value)
    
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(
    restaurant_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restoran tidak ditemukan")
    
    if db_restaurant.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Anda bukan pemilik restoran ini")
    
    db.delete(db_restaurant)
    db.commit()
    return None