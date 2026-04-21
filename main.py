from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db
from models import user as user_model
from models import restaurant as restaurant_model
from models import menu as menu_model
from schemas import user as user_schema
from schemas import restaurant as restaurant_schema
from schemas import menu as menu_schema
from auth.security import (
    get_password_hash, authenticate_user, create_access_token,
    get_current_active_user
)
from routers import restaurants, menus

# Buat tabel database
user_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hodo.id - API Katalog Restoran & Menu",
    description="Hodo.id adalah platform katalog restoran dan menu makanan & minuman.",
    version="1.0.0",
    contact={
        "name": "Ishmah Nurwasilah",
        "email": "h071241019@unhas.ac.id",
    }
)

# Include routers
app.include_router(restaurants.router)
app.include_router(menus.router)

@app.get("/")
def root():
    return {"message": "Welcome to Hodo.id API", "docs": "/docs"}

@app.post("/register", response_model=user_schema.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")
    hashed_password = get_password_hash(user.password)
    db_user = user_model.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=user_schema.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=user_schema.UserResponse)
def read_users_me(current_user = Depends(get_current_active_user)):
    return current_user

@app.get("/users", response_model=List[user_schema.UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Akses ditolak. Hanya admin.")
    users = db.query(user_model.User).all()
    return users