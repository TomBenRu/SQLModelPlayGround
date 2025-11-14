"""
Script zum Erstellen von vielen Testdaten für Performance-Tests.
"""
from sqlmodel import Session, select
from app.database import engine
from app.models.user import User
from app.models.post import Post
import random


def create_large_dataset():
    """Erstellt 100 User mit jeweils 5-10 Posts."""
    with Session(engine) as session:
        # Zuerst prüfen ob schon viele User existieren
        existing_count = len(session.exec(select(User)).all())
        if existing_count > 50:
            print(f"⚠️  Es existieren bereits {existing_count} User.")
            response = input("Trotzdem fortfahren? (y/n): ")
            if response.lower() != 'y':
                return

        print("📝 Erstelle 100 User mit Posts...")

        for i in range(100):
            # User erstellen
            user = User(
                name=f"user_{i}",
                email=f"user{i}@test.com"
            )
            session.add(user)
            session.commit()
            session.refresh(user)

            # 5-10 Posts pro User
            num_posts = random.randint(5, 10)
            for j in range(num_posts):
                post = Post(
                    title=f"Post {j} von {user.name}",
                    content=f"Das ist Post Nummer {j}",
                    published=random.choice([True, False]),
                    user_id=user.id
                )
                session.add(post)

            session.commit()

            if (i + 1) % 10 == 0:
                print(f"✅ {i + 1}/100 User erstellt...")

        print("🎉 Fertig! 100 User mit Posts erstellt.")


if __name__ == "__main__":
    create_large_dataset()