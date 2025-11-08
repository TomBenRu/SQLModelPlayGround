"""
FastAPI Application Entry Point
================================
Hier wird die FastAPI App initialisiert und gestartet.
"""

from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import users, posts


# FastAPI App erstellen
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Ein Lernprojekt für SqlModel mit PostgreSQL",
    debug=settings.DEBUG
)


# API Router einbinden
app.include_router(users.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1/posts", tags=["posts"])


@app.get("/")
async def root():
    """
    Health Check Endpoint
    
    Returns:
        dict: Status-Information
    """
    return {
        "message": "SQLModel Playground API",
        "version": settings.VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """
    Gesundheitscheck der Anwendung
    
    Returns:
        dict: Health Status
    """
    return {
        "status": "healthy",
        "database": "not connected yet"  # Wird in Modul 3 erweitert
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-Reload bei Code-Änderungen
    )
