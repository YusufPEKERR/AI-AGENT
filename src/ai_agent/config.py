import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Force loading of local .env file over system environment variables
load_dotenv(override=True)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # LLM Configuration
    openai_api_key: str
    openai_base_url: str = "https://integrate.api.nvidia.com/v1"
    model_name: str = "nvidia/nemotron-3-ultra-550b-a55b"
    reasoning_budget: int = 8192
    max_tokens: int = 8192
    temperature: float = 1.0
    top_p: float = 0.95

    # Runtime Configuration
    log_level: str = "INFO"
    max_tool_iterations: int = 10
    tool_timeout_seconds: int = 60
    enable_reasoning: bool = True

    # Security Guardrails
    allowed_paths: list[Path] = [Path.home()]
    allowed_commands: list[str] = [
        "git", "docker", "kubectl", "powershell", "cmd", "bash",
        "python", "pip", "npm", "dotnet", "go", "cargo", "wsl", "gofmt", "rustfmt", "npx"
    ]


settings = Settings()
