"""
SQLModel Modelle
================
Hier werden alle Datenbank-Modelle definiert.
"""

from app.models.user import User, UserCreate, UserRead, UserUpdate
from app.models.post import Post, PostCreate, PostRead, PostUpdate
from app.models.product import Product, ProductCreate, ProductRead, ProductUpdate

__all__ = [
    # User Models
    "User",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    # Post Models
    "Post",
    "PostCreate",
    "PostRead",
    "PostUpdate",
    # Product Models
    "Product",
    "ProductCreate",
    "ProductRead",
    "ProductUpdate",
]
