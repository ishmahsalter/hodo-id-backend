from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models.menu import Menu
from models.restaurant import Restaurant
from schemas.menu import MenuCreate, MenuResponse
from auth.security import get_current_active_user

router = APIRouter(prefix="/menus", tags=["Menus"])