"""E2B configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """E2B sandbox configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )

    # E2B configuration
    E2B_API_KEY: str = ""
    E2B_TEMPLATE: str = ""  # Empty = default code-interpreter template
    E2B_TIMEOUT: int = 30 * 60  # 30 minutes

    # R2 / S3 storage
    R2_ENDPOINT: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET: str = "manimo-notebooks"

    # LLM providers
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""


settings = Settings()
