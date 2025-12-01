import asyncio

from fastmcp import Client
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    access_token: SecretStr = Field(default=..., min_length=1)


async def main():
    settings = Settings()

    access_token = settings.access_token.get_secret_value()

    async with Client(
        "http://127.0.0.1:8000/mcp",
        auth=access_token,
    ) as client:
        await client.ping()


if __name__ == "__main__":
    asyncio.run(main())
