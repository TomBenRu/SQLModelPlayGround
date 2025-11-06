"""
Database Check Script
======================
Prüft die Datenbankverbindung und zeigt vorhandene Tabellen an.

Usage:
    python -m app.check_db
    
    oder mit uv:
    uv run python -m app.check_db
"""

from sqlalchemy import inspect, text
from app.database import engine
from app.core.config import settings


def check_db():
    """Prüft Datenbank-Status"""
    print("🔍 Prüfe Datenbank-Verbindung...\n")
    print(f"📊 Verbindung: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
    print(f"👤 User: {settings.POSTGRES_USER}\n")
    
    try:
        # Test der Verbindung
        with engine.connect() as conn:
            # PostgreSQL Version abfragen
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Verbindung erfolgreich!")
            print(f"🐘 PostgreSQL Version: {version.split(',')[0]}\n")
            
            # Tabellen auflisten
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"📋 Vorhandene Tabellen ({len(tables)}):")
                for table in tables:
                    columns = inspector.get_columns(table)
                    print(f"\n  📁 {table}")
                    print(f"     Spalten: {len(columns)}")
                    for col in columns:
                        col_type = str(col['type'])
                        nullable = "NULL" if col['nullable'] else "NOT NULL"
                        pk = " 🔑" if col.get('primary_key') else ""
                        print(f"       - {col['name']}: {col_type} {nullable}{pk}")
            else:
                print("⚠️ Keine Tabellen gefunden!")
                print("\n💡 Tipp: Führe 'python -m app.init_db' aus, um Tabellen zu erstellen.")
                
    except Exception as e:
        print(f"❌ Verbindungsfehler: {e}")
        print("\n🔧 Mögliche Lösungen:")
        print("  1. Ist PostgreSQL gestartet? (docker-compose up -d)")
        print("  2. Sind die Zugangsdaten korrekt? (siehe .env)")
        print("  3. Ist der Port erreichbar? (5432)")
        raise


if __name__ == "__main__":
    check_db()
