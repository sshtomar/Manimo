"""Application configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

    # API settings
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    def get_allowed_origins(self) -> list[str]:
        """Parse ALLOWED_ORIGINS as comma-separated list."""
        if isinstance(self.ALLOWED_ORIGINS, str):
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
        return self.ALLOWED_ORIGINS

    # LLM providers
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    DEFAULT_LLM_PROVIDER: str = "anthropic"
    DEFAULT_MODEL: str = "claude-haiku-4-5-20251001"

    # Dual-model strategy: Opus for planning/analysis, Sonnet for execution
    OPUS_MODEL: str = "claude-opus-4-5-20251101"
    SONNET_MODEL: str = "claude-sonnet-4-20250514"
    ENABLE_EXTENDED_THINKING: bool = False
    EXTENDED_THINKING_BUDGET: int = 2048
    ENABLE_INTERLEAVED_THINKING: bool = False

    # R2 / S3 storage
    R2_ENDPOINT: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET: str = "manimo-notebooks"

    # Modal
    MODAL_TOKEN_ID: str = ""
    MODAL_TOKEN_SECRET: str = ""

    # Auth (optional for MVP)
    JWT_SECRET_KEY: str = "dev-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"

    # Monitoring
    LOGFIRE_TOKEN: str = ""

    # Development/Testing
    USE_LOCAL_STORAGE: bool = False


settings = Settings()

