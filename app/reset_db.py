"""
Database Reset Script
=====================
Loescht alle Tabellen und erstellt sie neu.

ACHTUNG: Alle Daten gehen verloren!

Usage:
    python -m app.reset_db
    
    oder mit uv:
    uv run python -m app.reset_db
"""

from app.database import create_db_and_tables, drop_db_and_tables, engine
from app.core.config import settings


def reset_db():
    """Loescht und erstellt alle Tabellen neu"""
    print("="* 50)
    print("DATENBANK RESET")
    print("="* 50)
    print(f"Verbinde zu: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
    
    try:
        # Test der Verbindung
        with engine.connect() as conn:
            print("Datenbankverbindung erfolgreich!")
        
        # Tabellen loeschen
        print("\nLosche alle Tabellen...")
        drop_db_and_tables()
        
        # Tabellen neu erstellen
        print("\nErstelle Tabellen neu...")
        create_db_and_tables()
        
        print("\n" + "="* 50)
        print("DATENBANK ERFOLGREICH ZURUECKGESETZT!")
        print("="* 50)
        print("\nErstellte Tabellen:")
        print("  - users")
        print("  - posts")
        print("  - products")
        
    except Exception as e:
        print(f"\nFehler beim Reset: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    reset_db()
