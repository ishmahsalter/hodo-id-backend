from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models
from app import schemas
from app.auth import get_current_active_user

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

# GET semua restoran (public)
@router.get("/", response_model=List[schemas.RestaurantResponse])
def get_all_restaurants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    restaurants = db.query(models.Restaurant).offset(skip).limit(limit).all()
    return restaurants

# GET restoran by ID (public)
@router.get("/{restaurant_id}", response_model=schemas.RestaurantResponse)
def get_restaurant_by_id(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restoran tidak ditemukan")
    return restaurant

# POST restoran baru (login required)
@router.post("/", response_model=schemas.RestaurantResponse, status_code=status.HTTP_201_CREATED)
def create_restaurant(
    restaurant: schemas.RestaurantCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_restaurant = models.Restaurant(
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

# PUT update restoran (owner only)
@router.put("/{restaurant_id}", response_model=schemas.RestaurantResponse)
def update_restaurant(
    restaurant_id: int,
    restaurant_update: schemas.RestaurantCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restoran tidak ditemukan")
    
    if db_restaurant.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Anda bukan pemilik restoran ini")
    
    for key, value in restaurant_update.model_dump().items():
        setattr(db_restaurant, key, value)
    
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

# DELETE restoran (owner only)
@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(
    restaurant_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restoran tidak ditemukan")
    
    if db_restaurant.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Anda bukan pemilik restoran ini")
    
    db.delete(db_restaurant)
    db.commit()
    return None