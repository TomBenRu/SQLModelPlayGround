"""
Create Test Data Script
=======================
Erstellt Testdaten für User und Posts mit Relationships.

Usage:
    python -m app.create_testdata
    
    oder mit uv:
    uv run python -m app.create_testdata
"""

from sqlmodel import Session

from app.database import engine
from app.models import User, UserCreate, Post, PostCreate


def create_test_data():
    """Erstellt Testdaten: Users und ihre Posts"""
    print("="* 50)
    print("TESTDATEN ERSTELLEN")
    print("="* 50)
    
    with Session(engine) as session:
        # User 1 erstellen
        user1 = User(
            name="Alice Schmidt",
            email="alice@example.com",
            is_active=True
        )
        session.add(user1)
        session.commit()
        session.refresh(user1)
        print(f"\nUser erstellt: {user1.name} (ID: {user1.id})")
        
        # User 2 erstellen
        user2 = User(
            name="Bob Mueller",
            email="bob@example.com",
            is_active=True
        )
        session.add(user2)
        session.commit()
        session.refresh(user2)
        print(f"User erstellt: {user2.name} (ID: {user2.id})")
        
        # User 3 erstellen
        user3 = User(
            name="Charlie Weber",
            email="charlie@example.com",
            is_active=False
        )
        session.add(user3)
        session.commit()
        session.refresh(user3)
        print(f"User erstellt: {user3.name} (ID: {user3.id})")
        
        # Posts für User 1 (Alice)
        post1 = Post(
            title="Mein erster Blog-Post",
            content="Das ist ein spannender erster Post über SqlModel und FastAPI.",
            published=True,
            user_id=user1.id
        )
        session.add(post1)
        
        post2 = Post(
            title="Relationships in SqlModel",
            content="Heute lernen wir, wie One-to-Many Beziehungen funktionieren.",
            published=True,
            user_id=user1.id
        )
        session.add(post2)
        
        post3 = Post(
            title="Draft: Noch nicht fertig",
            content="Dieser Post ist noch nicht veröffentlicht.",
            published=False,
            user_id=user1.id
        )
        session.add(post3)
        
        # Posts für User 2 (Bob)
        post4 = Post(
            title="FastAPI ist großartig",
            content="FastAPI macht so viel Spaß! Besonders mit SqlModel.",
            published=True,
            user_id=user2.id
        )
        session.add(post4)
        
        post5 = Post(
            title="PostgreSQL und Docker",
            content="Wie man PostgreSQL mit Docker Compose aufsetzt.",
            published=True,
            user_id=user2.id
        )
        session.add(post5)
        
        # Ein Post für User 3 (Charlie) - inaktiver User
        post6 = Post(
            title="Inaktiver User Post",
            content="Dieser Post gehört zu einem inaktiven User.",
            published=False,
            user_id=user3.id
        )
        session.add(post6)
        
        session.commit()
        
        print(f"\n{6} Posts erstellt:")
        print(f"  - {3} Posts von {user1.name}")
        print(f"  - {2} Posts von {user2.name}")
        print(f"  - {1} Post von {user3.name}")
        
        print("\n" + "="* 50)
        print("TESTDATEN ERFOLGREICH ERSTELLT!")
        print("="* 50)
        print("\nDu kannst jetzt die API testen:")
        print("  GET  http://localhost:8000/api/v1/users/")
        print("  GET  http://localhost:8000/api/v1/posts/")
        print(f"  GET  http://localhost:8000/api/v1/users/{user1.id}/posts")
        print(f"  GET  http://localhost:8000/api/v1/posts/1")
        print("\nOder öffne: http://localhost:8000/docs")


if __name__ == "__main__":
    try:
        create_test_data()
    except Exception as e:
        print(f"\nFehler beim Erstellen der Testdaten: {e}")
        import traceback
        traceback.print_exc()
        raise
