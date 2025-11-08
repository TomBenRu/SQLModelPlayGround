"""
SQLModel Modelle
================
Hier werden alle Datenbank-Modelle definiert.
"""

from app.models.user import User, UserCreate, UserRead, UserUpdate, UserReadWithPosts, rebuild_models as rebuild_user_models
from app.models.post import Post, PostCreate, PostRead, PostUpdate, PostReadWithAuthor, rebuild_models as rebuild_post_models
from app.models.product import Product, ProductCreate, ProductRead, ProductUpdate

rebuild_user_models()
rebuild_post_models()

__all__ = [
    # User Models
    "User",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "UserReadWithPosts",
    # Post Models
    "Post",
    "PostCreate",
    "PostRead",
    "PostUpdate",
    "PostReadWithAuthor",
    # Product Models
    "Product",
    "ProductCreate",
    "ProductRead",
    "ProductUpdate",
]
