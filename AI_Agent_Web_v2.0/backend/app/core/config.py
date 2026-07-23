from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    database_url: str = "sqlite:///./app_data.db"
    openai_api_key: str = "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"
    openai_base_url: str = "https://integrate.api.nvidia.com/v1"
    model_name: str = "nvidia/nemotron-3-ultra-550b-a55b"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"


settings = Settings()
