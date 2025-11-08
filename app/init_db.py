"""
Database Initialization Script
================================
Erstellt alle Datenbank-Tabellen.

Usage:
    python -m app.init_db
    
    oder mit uv:
    uv run python -m app.init_db
"""

from app.database import create_db_and_tables, engine
from app.core.config import settings


def init_db():
    """Initialisiert die Datenbank"""
    print("Initialisiere Datenbank...")
    print(f"Verbinde zu: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
    
    try:
        # Test der Verbindung
        with engine.connect() as conn:
            print("Datenbankverbindung erfolgreich!")
        
        # Tabellen erstellen
        create_db_and_tables()
        
        print("\nDatenbank wurde erfolgreich initialisiert!")
        print("\nErstellte Tabellen:")
        print("  - users")
        print("  - posts")
        print("  - products")
        
    except Exception as e:
        print(f"\nFehler bei der Initialisierung: {e}")
        raise


if __name__ == "__main__":
    init_db()
