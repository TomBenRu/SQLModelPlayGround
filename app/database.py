"""
Datenbank-Verbindung
====================
Setup für SQLModel Engine und Session Management.
"""

from sqlmodel import Session, create_engine
from app.core.config import settings


# Engine erstellen
# echo=True zeigt alle SQL-Statements in der Console (gut zum Lernen!)
engine = create_engine(
    settings.database_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,  # Prüft Verbindung vor Nutzung
    pool_size=5,         # Max. 5 Verbindungen im Pool
    max_overflow=10      # Max. 10 zusätzliche Verbindungen bei Bedarf
)


def get_session():
    """
    Session Factory für Dependency Injection in FastAPI.
    
    Verwendung in FastAPI:
    ```python
    @app.get("/items")
    def get_items(session: Session = Depends(get_session)):
        ...
    ```
    
    Yields:
        Session: Eine SQLModel Session
    """
    with Session(engine) as session:
        yield session
