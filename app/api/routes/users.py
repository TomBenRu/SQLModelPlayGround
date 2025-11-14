"""
User API Routes
===============
CRUD-Endpunkte für User-Verwaltung.

Demonstriert:
- CREATE: User erstellen (POST)
- Dependency Injection (Session)
- Request/Response Models
- Error Handling
- HTTP Status Codes
"""

import datetime
from time import perf_counter

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlmodel import Session, select, SQLModel, desc, Field

from app.database import get_session
from app.models.user import User, UserCreate, UserRead, UserUpdate, UserStats
from app.models.post import Post, PostRead


# Router erstellen mit Prefix und Tags für Swagger UI
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Neuen User erstellen",
    description="Erstellt einen neuen User in der Datenbank."
)
def create_user(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Erstellt einen neuen User.
    
    Args:
        user: UserCreate Modell mit User-Daten
        session: Datenbank-Session (wird automatisch injiziert)
    
    Returns:
        UserRead: Der erstellte User mit ID und Timestamps
    
    Raises:
        HTTPException 409: Wenn Email bereits existiert
    """
    
    # Prüfen, ob Email bereits existiert
    existing_user = session.exec(
        select(User).where(User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user.email}' already exists"
        )
    
    # User-Objekt erstellen
    db_user = User.model_validate(user)
    
    # In Datenbank speichern
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user



@router.get(
    "/",
    response_model=list[UserRead],
    summary="Alle User abrufen",
    description="Ruft eine Liste aller User ab mit optionaler Pagination."
)
def get_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """
    Ruft eine Liste aller User ab.
    
    Args:
        skip: Anzahl der zu überspringenden Einträge (für Pagination)
        limit: Maximale Anzahl der zurückzugebenden Einträge
        session: Datenbank-Session (wird automatisch injiziert)
    
    Returns:
        list[UserRead]: Liste aller User
    """
    
    # Alle User mit Pagination abrufen
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    
    return users


@router.get(
    "/stats",
    response_model=list[UserStats],
    summary="User-Statistiken abrufen",
    description="Gibt alle User mit Anzahl ihrer Posts zurück."
)
def get_user_stats(
    session: Session = Depends(get_session)
):
    """
    Gibt alle User mit Anzahl ihrer Posts zurück.

    Parameters:
        - **session**: Datenbank-Session (wird automatisch injiziert)

    Returns:
        list[UserStats]: Liste von User-Statistiken
    """

    t0 = perf_counter()

    # # Weg 1: Relationship nutzen (ineffizient bei vielen Usern)
    # users = session.exec(select(User)).all()
    # user_stats = []
    # for user in users:
    #     post_count = len(user.posts)  # Greift auf Relationship zu
    #     user_stats.append(UserStats(
    #         id=user.id,
    #         name=user.name,
    #         email=user.email,
    #         post_count=post_count
    #     ))

    # Weg 2: Query mit JOIN und COUNT (effizienter bei vielen Usern)
    statement = (
        select(User.id, User.name, User.email, func.count(Post.id).label("post_count"))
        .join(Post, isouter=True)
        .group_by(User.id)
        .order_by(desc("post_count"))
    )
    user_stats = [
        UserStats(
            id=row.id,
            username=row.name,
            email=row.email,
            post_count=row.post_count
        )
        for row in session.exec(statement).all()
    ]

    print(f"Query-Dauer: {perf_counter() - t0:.2f} Sekunden")

    return user_stats


@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="User nach ID abrufen",
    description="Ruft einen einzelnen User anhand seiner ID ab."
)
def get_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    """
    Ruft einen User anhand seiner ID ab.
    
    Args:
        user_id: Die ID des Users
        session: Datenbank-Session (wird automatisch injiziert)
    
    Returns:
        UserRead: Der gefundene User
    
    Raises:
        HTTPException 404: Wenn User nicht gefunden wurde
    """
    
    # User aus Datenbank abrufen
    user = session.get(User, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    return user



@router.patch(
    "/{user_id}",
    response_model=UserRead,
    summary="User aktualisieren",
    description="Aktualisiert einen User teilweise (Partial Update)."
)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session)
):
    """
    Aktualisiert einen User teilweise.
    
    Nur die übergebenen Felder werden aktualisiert (Partial Update).
    Das updated_at Feld wird automatisch gesetzt.
    
    Args:
        user_id: Die ID des zu aktualisierenden Users
        user_update: UserUpdate Modell mit zu ändernden Feldern
        session: Datenbank-Session (wird automatisch injiziert)
    
    Returns:
        UserRead: Der aktualisierte User
    
    Raises:
        HTTPException 404: Wenn User nicht gefunden wurde
        HTTPException 409: Wenn neue Email bereits existiert
    """
    
    # User aus Datenbank abrufen
    db_user = session.get(User, user_id)
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Nur gesetzte Felder extrahieren (exclude_unset=True)
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Wenn Email geändert wird, prüfen ob sie bereits existiert
    if "email" in update_data:
        existing_user = session.exec(
            select(User).where(
                User.email == update_data["email"],
                User.id != user_id  # Nicht den aktuellen User prüfen
            )
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email '{update_data['email']}' already exists"
            )
    
    # Felder aktualisieren
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    # updated_at Timestamp setzen
    db_user.updated_at = datetime.datetime.now(datetime.UTC)
    
    # In Datenbank speichern (session.add() nicht nötig, da Objekt bereits getrackt wird)
    session.commit()
    session.refresh(db_user)
    
    return db_user



@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="User löschen",
    description="Löscht einen User permanent aus der Datenbank (Hard Delete)."
)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    """
    Löscht einen User permanent aus der Datenbank.
    
    Dies ist ein Hard Delete - der Datensatz wird physisch aus der
    Datenbank entfernt und kann nicht wiederhergestellt werden.
    
    Args:
        user_id: Die ID des zu löschenden Users
        session: Datenbank-Session (wird automatisch injiziert)
    
    Returns:
        None (204 No Content)
    
    Raises:
        HTTPException 404: Wenn User nicht gefunden wurde
    """
    
    # User aus Datenbank abrufen
    db_user = session.get(User, user_id)
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # User löschen (session.delete() funktioniert wie session.add() - Objekt wird getrackt)
    session.delete(db_user)
    session.commit()



@router.get(
    "/{user_id}/posts",
    response_model=list[PostRead],
    summary="Posts eines Users abrufen",
    description="Gibt alle Posts eines bestimmten Users zurück."
)
def get_user_posts(
    user_id: int,
    session: Session = Depends(get_session),
    skip: int = Query(default=0, ge=0, description="Anzahl zu überspringender Posts"),
    limit: int = Query(default=20, ge=1, le=100, description="Max. Anzahl zurückzugebender Posts")
):
    """
    Gibt alle Posts eines Users zurück.
    
    Parameters:
        - **user_id**: ID des Users
        - **skip**: Anzahl zu überspringender Posts (für Pagination)
        - **limit**: Maximale Anzahl zurückzugebender Posts (1-100)
    
    Returns:
        list[PostRead]: Liste von Posts des Users
    
    Raises:
        404: User mit der angegebenen ID existiert nicht
    """
    # Prüfen ob User existiert
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Posts des Users abrufen
    statement = select(Post).where(Post.user_id == user_id).offset(skip).limit(limit)
    posts = session.exec(statement).all()
    
    return posts
    
    # Kein Return bei 204 No Content
