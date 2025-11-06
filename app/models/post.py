"""
Post Model
==========
Einfaches Blog-Post Modell.

Demonstriert:
- Einfachere SqlModel-Struktur
- Text-Felder
- Optional vs. Required Fields
"""

import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class PostBase(SQLModel):
    """Gemeinsame Post-Felder"""
    
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Titel des Posts"
    )
    
    content: str = Field(
        description="Inhalt des Posts"
    )
    
    published: bool = Field(
        default=False,
        description="Ist der Post veröffentlicht?"
    )


class Post(PostBase, table=True):
    """
    Post-Tabelle in der Datenbank.
    
    Hinweis: In Modul 6 fügen wir eine Beziehung zu User hinzu.
    """
    
    __tablename__ = "posts"
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )
    
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
    
    # Später: Foreign Key zu User
    # user_id: Optional[int] = Field(default=None, foreign_key="users.id")


class PostCreate(PostBase):
    """Modell für Post-Erstellung"""
    pass


class PostRead(PostBase):
    """Modell für Post-Rückgabe"""
    
    id: int
    created_at: datetime.datetime


class PostUpdate(SQLModel):
    """Modell für Post-Updates (alle Felder optional)"""
    
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200
    )
    
    content: Optional[str] = None
    published: Optional[bool] = None
