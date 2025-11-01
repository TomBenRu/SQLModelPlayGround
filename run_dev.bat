@echo off
REM FastAPI Development Server starten
echo Starting SQLModel Playground API...
echo.
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
