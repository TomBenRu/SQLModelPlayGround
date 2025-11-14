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
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User, UserRead


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
    
    Relationship: Gehört zu einem User (author).
    """
    
    __tablename__ = "posts"
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )
    
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
    
    # Foreign Key zu User
    user_id: int = Field(
        foreign_key="users.id",
        description="ID des Post-Autors"
    )
    
    # Relationship zum User (bidirektional)
    author: "User" = Relationship(back_populates="posts")


class PostCreate(PostBase):
    """
    Modell für Post-Erstellung.
    
    User-ID muss beim Erstellen angegeben werden.
    """
    user_id: int


class PostRead(PostBase):
    """
    Modell für Post-Rückgabe (ohne Author-Details).
    """
    
    id: int
    created_at: datetime.datetime
    user_id: int


class PostUpdate(SQLModel):
    """Modell für Post-Updates (alle Felder optional)"""
    
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200
    )
    
    content: Optional[str] = None
    published: Optional[bool] = None


class PostReadWithAuthor(PostRead):
    """
    Modell für Post-Rückgabe MIT Author-Details.
    
    Enthält vollständige User-Daten des Autors.
    Ideal für Detail-Ansichten eines Posts.
    """
    
    author: "UserRead"


class PaginatedPostResponse(SQLModel):
    items: list[PostRead]
    total: int
    page: int
    page_size: int
    total_pages: int


def rebuild_models():
    from .user import UserRead
    PostReadWithAuthor.model_rebuild()
