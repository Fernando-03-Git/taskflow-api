from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    app_version: str
    debug: bool
    
    # Base de datos
    database_url: str
    
    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

# Instancia única que usa toda la app
settings = Settings()