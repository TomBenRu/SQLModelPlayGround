# SQLModel Playground 🚀

Ein Lernprojekt für **SqlModel** mit **PostgreSQL** und **FastAPI**.

## 📋 Projekt-Übersicht

Dieses Projekt dient als praktischer Grundlagenkurs für:
- SqlModel für ORM (Object-Relational Mapping)
- PostgreSQL als Datenbank
- FastAPI als Web-Framework
- Best Practices für Projektstruktur

## 🏗️ Projektstruktur

```
SQLModelPlayGround/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI Entry Point
│   ├── database.py          # DB Connection & Session
│   ├── models/              # SqlModel Modelle
│   │   └── __init__.py
│   ├── api/                 # API Routes
│   │   └── __init__.py
│   └── core/
│       └── config.py        # Konfiguration
├── tests/                   # Test Suite
├── docker-compose.yml       # PostgreSQL Container
├── pyproject.toml          # Dependencies
└── README.md
```

## 🚀 Setup & Installation

### 1. Dependencies installieren

```bash
uv sync
```

Dies installiert automatisch alle Dependencies aus der `pyproject.toml`.

### 2. PostgreSQL mit Docker starten

```bash
docker-compose up -d
```

Prüfen ob Container läuft:
```bash
docker ps
```

### 3. Umgebungsvariablen konfigurieren

```bash
copy .env.example .env
```

*(Auf Linux/Mac: `cp .env.example .env`)*

### 4. FastAPI Server starten

**Windows (einfach):**
```bash
run_dev.bat
```

**Oder direkt mit uvicorn:**
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. API testen

- **API Docs:** http://localhost:8000/docs
- **Root Endpoint:** http://localhost:8000/
- **Health Check:** http://localhost:8000/health

## 🧪 Tests ausführen

```bash
uv run pytest
```

## 📚 Lernmodule

- [x] **Modul 1:** Projektsetup & Umgebung ✅
- [ ] **Modul 2:** SqlModel Grundlagen
- [ ] **Modul 3:** Datenbank-Verbindung
- [ ] **Modul 4:** Tabellenerstellung & Migration
- [ ] **Modul 5:** CRUD-Operationen
- [ ] **Modul 6:** Beziehungen (Relationships)
- [ ] **Modul 7:** FastAPI Integration
- [ ] **Modul 8:** Testing & Best Practices

## 🛠️ Nützliche Befehle

### Docker Commands

```bash
# Container starten
docker-compose up -d

# Container stoppen
docker-compose down

# Logs anzeigen
docker-compose logs -f

# PostgreSQL Shell öffnen
docker exec -it sqlmodel_playground_db psql -U playground_user -d playground_db
```

### Database Commands (in psql)

```sql
-- Alle Tabellen anzeigen
\dt

-- Tabellenstruktur anzeigen
\d <tablename>

-- Datenbank wechseln
\c playground_db

-- Quit
\q
```

## 📖 Ressourcen

- [SqlModel Docs](https://sqlmodel.tiangolo.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

## 📝 Lizenz

Dieses Projekt dient ausschließlich Lernzwecken.
