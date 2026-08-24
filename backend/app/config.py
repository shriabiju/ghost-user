from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central app configuration, loaded from environment variables / .env file.
    """

    database_url: str = "postgresql://user:password@localhost:5432/ghostuser"
    groq_api_key: str = ""
    frontend_origin: str = "http://localhost:5173"

    # Agent behavior tuning
    max_steps_per_session: int = 12
    groq_model: str = "openai/gpt-oss-120b"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()