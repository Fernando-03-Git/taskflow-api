from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env") 
    
    app_name: str
    app_version: str
    debug: bool
    
    # Base de datos
    database_url: str
    
    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


# Instancia única que usa toda la app
settings = Settings()