from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, get_db
from app import models
from app import schemas
from app.auth import (
    get_password_hash, authenticate_user, create_access_token,
    get_current_active_user
)
from app.routers import restaurants, menus

# Buat tabel database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hodo.id - API Katalog Restoran & Menu",
    description="""
Hodo.id adalah platform katalog restoran dan menu makanan & minuman.

Fitur yang tersedia:

- Registrasi dan login dengan JWT
- CRUD Restoran (Create, Read, Update, Delete)
- CRUD Menu (makanan & minuman)
- Filter menu berdasarkan kategori (Makanan / Minuman)
- Proteksi endpoint dengan autentikasi JWT
- Role-based access control (User & Admin)

Role dalam sistem:
- User: Dapat melihat restoran & menu, serta membuat restoran sendiri
- Admin: Dapat mengelola semua data (termasuk menghapus restoran milik user lain)

Dibangun dengan:
- FastAPI (backend framework)
- SQLAlchemy (ORM)
- SQLite (database)
- JWT (autentikasi)
    """,
    version="1.0.0",
    contact={
        "name": "Ishmah Nurwasilah",
        "email": "h071241019@unhas.ac.id",
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(restaurants.router)
app.include_router(menus.router)

# ==================== ROOT ENDPOINT ====================

@app.get("/")
def root():
    return {
        "message": "Welcome to Hodo.id API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# ==================== AUTH ENDPOINTS ====================

@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=schemas.Token)
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

# ==================== USER ENDPOINTS ====================

@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user = Depends(get_current_active_user)):
    return current_user

@app.get("/users", response_model=List[schemas.UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Akses ditolak. Hanya admin.")
    users = db.query(models.User).all()
    return users