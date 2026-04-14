from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import models
from app import schemas
from app.auth import get_current_active_user

router = APIRouter(prefix="/menus", tags=["Menus"])

# GET semua menu (public) + filter kategori
@router.get("/", response_model=List[schemas.MenuResponse])
def get_all_menus(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Menu)
    if category:
        query = query.filter(models.Menu.category == category)
    menus = query.offset(skip).limit(limit).all()
    return menus

# GET menu by ID (public)
@router.get("/{menu_id}", response_model=schemas.MenuResponse)
def get_menu_by_id(
    menu_id: int,
    db: Session = Depends(get_db)
):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu tidak ditemukan")
    return menu

# POST menu baru (login required, cek owner resto)
@router.post("/", response_model=schemas.MenuResponse, status_code=status.HTTP_201_CREATED)
def create_menu(
    menu: schemas.MenuCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == menu.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restoran tidak ditemukan")
    
    if restaurant.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Anda bukan pemilik restoran ini")
    
    db_menu = models.Menu(
        name=menu.name,
        description=menu.description,
        price=menu.price,
        category=menu.category,
        image_url=menu.image_url,
        restaurant_id=menu.restaurant_id
    )
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

# PUT update menu (owner resto)
@router.put("/{menu_id}", response_model=schemas.MenuResponse)
def update_menu(
    menu_id: int,
    menu_update: schemas.MenuCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu tidak ditemukan")
    
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == db_menu.restaurant_id).first()
    if restaurant.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Anda bukan pemilik restoran ini")
    
    for key, value in menu_update.model_dump().items():
        setattr(db_menu, key, value)
    
    db.commit()
    db.refresh(db_menu)
    return db_menu

# DELETE menu (owner resto)
@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(
    menu_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu tidak ditemukan")
    
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == db_menu.restaurant_id).first()
    if restaurant.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Anda bukan pemilik restoran ini")
    
    db.delete(db_menu)
    db.commit()
    return None

# GET menu by restaurant (public)
@router.get("/restaurant/{restaurant_id}", response_model=List[schemas.MenuResponse])
def get_menus_by_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restoran tidak ditemukan")
    return restaurant.menus