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

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models.user import User, UserCreate, UserRead, UserUpdate


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
    
    # Kein Return bei 204 No Content
