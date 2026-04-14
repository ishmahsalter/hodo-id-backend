from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# Model User (untuk autentikasi JWT)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")  # admin, user

    # Relasi One-to-Many: User memiliki banyak Restoran
    restaurants = relationship("Restaurant", back_populates="owner")

# Model Restoran (entitas pertama)
class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    address = Column(String)
    phone = Column(String)
    image_url = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relasi Many-to-One: Restoran milik satu User
    owner = relationship("User", back_populates="restaurants")
    # Relasi One-to-Many: Restoran memiliki banyak Menu
    menus = relationship("Menu", back_populates="restaurant", cascade="all, delete-orphan")

# Model Menu (entitas kedua)
class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    category = Column(String)  # Makanan atau Minuman
    image_url = Column(String, nullable=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))

    # Relasi Many-to-One: Menu milik satu Restoran
    restaurant = relationship("Restaurant", back_populates="menus")