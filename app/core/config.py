"""
Konfiguration
=============
Zentrale Konfiguration für die Anwendung mit pydantic-settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Anwendungs-Konfiguration
    
    Kann über Umgebungsvariablen oder .env-Datei überschrieben werden.
    """
    
    # Datenbank
    POSTGRES_USER: str = "playground_user"
    POSTGRES_PASSWORD: str = "playground_pass"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "playground_db"
    
    # FastAPI
    PROJECT_NAME: str = "SQLModel Playground"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Development
    DEBUG: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )
    
    @property
    def database_url(self) -> str:
        """
        Baut die PostgreSQL Connection URL zusammen.
        
        Format: postgresql://user:password@host:port/database
        """
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


# Singleton-Instanz
settings = Settings()
