"""
Datenbank-Verbindung
====================
Setup für SQLModel Engine und Session Management.
"""

from sqlmodel import Session, SQLModel, create_engine
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



def create_db_and_tables():
    """
    Erstellt alle Tabellen in der Datenbank.
    
    Durchsucht alle SqlModel-Klassen mit `table=True` und
    erstellt die entsprechenden Tabellen in PostgreSQL.
    
    Wichtig: Die Modelle müssen importiert sein, damit
    SQLModel sie finden kann!
    """
    # Import aller Modelle, damit sie in SQLModel.metadata registriert sind
    from app.models import User, Post, Product  # noqa: F401
    
    SQLModel.metadata.create_all(engine)
    print("✅ Datenbank-Tabellen wurden erstellt!")


def drop_db_and_tables():
    """
    Löscht ALLE Tabellen aus der Datenbank.
    
    ⚠️ ACHTUNG: Alle Daten gehen verloren!
    Nur für Development/Testing verwenden!
    """
    from app.models import User, Post, Product  # noqa: F401
    
    SQLModel.metadata.drop_all(engine)
    print("⚠️ Alle Tabellen wurden gelöscht!")
