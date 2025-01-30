from typing import List
from pydantic_settings import BaseSettings
import logging


class Settings(BaseSettings):
    # Admin settings
    admin_api_key: str = "change-me-in-production"

    # CORS settings
    allowed_origins: List[str] = [
        "http://localhost:5173",  # SvelteKit dev server
        "http://localhost:4173",  # SvelteKit preview
    ]
    allow_credentials: bool = True
    allowed_methods: List[str] = ["*"]
    allowed_headers: List[str] = ["*"]

    # Logging settings
    log_level: str = "INFO"
    log_file: str = "api.log"
    log_max_size: int = 10 * 1024 * 1024  # 10 MB
    log_backup_count: int = 5

    class Config:
        env_prefix = "GOOD_DATES_"
        case_sensitive = False

    @property
    def log_level_enum(self) -> int:
        return getattr(logging, self.log_level.upper())


settings = Settings()
