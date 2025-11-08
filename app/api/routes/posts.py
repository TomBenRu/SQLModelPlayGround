"""
Post API Routes
===============
CRUD Endpoints für Posts mit Relationships zu Users.
"""

import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Post, PostCreate, PostRead, PostReadWithAuthor, PostUpdate, User

router = APIRouter()


@router.post(
    "/",
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED,
    summary="Post erstellen",
    description="Erstellt einen neuen Post für einen bestimmten User."
)
def create_post(
    post: PostCreate,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Erstellt einen neuen Post.
    
    - **title**: Titel des Posts (1-200 Zeichen)
    - **content**: Inhalt des Posts
    - **published**: Ist der Post veröffentlicht? (Default: False)
    - **user_id**: ID des Autors (muss existieren)
    
    Returns:
        PostRead: Der erstellte Post mit ID und Timestamp
    
    Raises:
        404: User mit der angegebenen ID existiert nicht
    """
    # Prüfen ob User existiert
    db_user = session.get(User, post.user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User mit ID {post.user_id} nicht gefunden"
        )
    
    # Post erstellen
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    
    return db_post


@router.get(
    "/",
    response_model=list[PostRead],
    summary="Alle Posts abrufen",
    description="Gibt eine Liste aller Posts zurück mit Pagination."
)
def get_posts(
    session: Session = Depends(get_session),
    skip: int = Query(default=0, ge=0, description="Anzahl zu überspringender Posts"),
    limit: int = Query(default=20, ge=1, le=100, description="Max. Anzahl zurückzugebender Posts")
):
    """
    Gibt eine Liste aller Posts zurück.
    
    Parameters:
        - **skip**: Anzahl zu überspringender Posts (für Pagination)
        - **limit**: Maximale Anzahl zurückzugebender Posts (1-100)
    
    Returns:
        list[PostRead]: Liste von Posts
    """
    statement = select(Post).offset(skip).limit(limit)
    posts = session.exec(statement).all()
    return posts


@router.get(
    "/{post_id}",
    response_model=PostReadWithAuthor,
    summary="Post mit Author-Details abrufen",
    description="Gibt einen einzelnen Post mit vollständigen Author-Informationen zurück."
)
def get_post(
    post_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Gibt einen Post mit Author-Details zurück.
    
    Parameters:
        - **post_id**: ID des Posts
    
    Returns:
        PostReadWithAuthor: Post mit eingebetteten User-Daten
    
    Raises:
        404: Post mit der angegebenen ID existiert nicht
    """
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post mit ID {post_id} nicht gefunden"
        )
    
    return db_post


@router.patch(
    "/{post_id}",
    response_model=PostRead,
    summary="Post aktualisieren",
    description="Aktualisiert einen bestehenden Post. user_id kann nicht geändert werden."
)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Aktualisiert einen Post (Partial Update).
    
    Nur die übergebenen Felder werden aktualisiert.
    Der Autor (user_id) kann nicht geändert werden.
    
    Parameters:
        - **post_id**: ID des zu aktualisierenden Posts
        - **title**: Neuer Titel (optional)
        - **content**: Neuer Inhalt (optional)
        - **published**: Neuer Status (optional)
    
    Returns:
        PostRead: Der aktualisierte Post
    
    Raises:
        404: Post mit der angegebenen ID existiert nicht
    """
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post mit ID {post_id} nicht gefunden"
        )
    
    # Nur übergebene Felder aktualisieren
    post_data = post_update.model_dump(exclude_unset=True)
    
    for key, value in post_data.items():
        setattr(db_post, key, value)
    
    session.commit()
    session.refresh(db_post)
    
    return db_post


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Post löschen",
    description="Löscht einen Post permanent aus der Datenbank."
)
def delete_post(
    post_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Löscht einen Post.
    
    Parameters:
        - **post_id**: ID des zu löschenden Posts
    
    Returns:
        204 No Content
    
    Raises:
        404: Post mit der angegebenen ID existiert nicht
    """
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post mit ID {post_id} nicht gefunden"
        )
    
    session.delete(db_post)
    session.commit()
    
    return None
