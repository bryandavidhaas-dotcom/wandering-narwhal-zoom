from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = True
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    DATABASE_URL: str = "your_mongodb_connection_string_here"
    AI_API_KEY: str = "your_anthropic_api_key_here"
    JWT_SECRET_KEY: str = "a_very_secret_key_that_should_be_changed"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

def get_settings() -> Settings:
    """Get application settings"""
    return settings