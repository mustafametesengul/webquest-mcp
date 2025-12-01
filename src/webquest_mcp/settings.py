from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        cli_parse_args=True,
    )
    auth_secret: SecretStr | None = Field(default=None, min_length=1)
    auth_audience: str | None = Field(default="webquest-mcp", min_length=1)
    openai_api_key: SecretStr | None = Field(default=None)
    hyperbrowser_api_key: SecretStr | None = Field(default=None)
    ngrok_authtoken: SecretStr | None = Field(default=None)
    port: int = Field(default=8000, ge=1, le=65535)


_settings = Settings()


def get_settings() -> Settings:
    global _settings
    return _settings
