"""
User Model
==========
Basis-Modell für User-Verwaltung.

Demonstriert:
- SqlModel Grundlagen
- Field-Validierung
- Indizes
- Timestamps
- API-Modelle (Create/Read)
"""

import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .post import Post, PostRead


class UserBase(SQLModel):
    """
    Basis-Klasse mit gemeinsamen User-Feldern.
    
    Diese Felder werden sowohl in der Datenbank als auch
    in den API-Modellen verwendet (DRY-Prinzip).
    """
    
    name: str = Field(
        min_length=1,
        max_length=100,
        description="Vollständiger Name des Users"
    )
    
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="Eindeutige E-Mail-Adresse",
        regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )
    
    is_active: bool = Field(
        default=True,
        description="Ist der User aktiv?"
    )


class User(UserBase, table=True):
    """
    User-Tabelle in der Datenbank.
    
    Erbt alle Felder von UserBase und fügt DB-spezifische
    Felder hinzu (ID, Timestamps).
    
    Relationship: Hat viele Posts (One-to-Many).
    """
    
    __tablename__ = "users"
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Eindeutige User-ID (auto-increment)"
    )
    
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="Zeitpunkt der Erstellung"
    )
    
    updated_at: Optional[datetime.datetime] = Field(
        default=None,
        description="Zeitpunkt der letzten Änderung"
    )
    
    # Relationship zu Posts (One-to-Many)
    posts: list["Post"] = Relationship(back_populates="author")


class UserCreate(UserBase):
    """
    Modell für User-Erstellung (API Request).
    
    Enthält nur die Felder, die beim Erstellen angegeben werden müssen.
    ID und Timestamps werden automatisch generiert.
    """
    pass


class UserRead(UserBase):
    """
    Modell für User-Rückgabe (API Response).
    
    Enthält alle Felder inklusive ID und Timestamps.
    """
    
    id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None


class UserUpdate(SQLModel):
    """
    Modell für User-Updates (API Request).
    
    Alle Felder sind optional, damit nur die gewünschten
    Felder aktualisiert werden müssen.
    """
    
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100
    )
    
    email: Optional[str] = Field(
        default=None,
        max_length=255,
        regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )
    
    is_active: Optional[bool] = None


class UserReadWithPosts(UserRead):
    """
    Modell für User-Rückgabe MIT allen Posts.
    
    Enthält vollständige Liste aller Posts des Users.
    Ideal für Profil-Ansichten oder User-Details.
    """
    
    posts: list["PostRead"] = []


def rebuild_models():
    from .post import PostRead
    UserReadWithPosts.model_rebuild()


