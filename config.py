from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "Book Publication Workflow"
    redis_url: str = "redis://localhost:6379"
    debug: bool = False
    api_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"

settings = Settings()
