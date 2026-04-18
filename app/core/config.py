from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    app_version: str
    debug: bool
    secret_key: str
    database_url: str

    class Config:
        env_file = ".env"

# Instancia única que usa toda la app
settings = Settings()