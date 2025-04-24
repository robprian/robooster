from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Bot settings
    BOT_TOKEN: str
    ADMIN_USER_ID: int
    
    # Database settings
    DATABASE_URL: str = "postgres://postgres:flyyZoaAZuX3EfQ@askkia.flycast:5432/postgres"
    
    # Google API settings
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create global settings instance
settings = Settings()