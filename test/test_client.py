import asyncio

from openai import AsyncOpenAI
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    client_access_token: SecretStr = Field(default=...)
    client_url: str = Field(default="http://127.0.0.1:8000/mcp")
    openai_api_key: SecretStr = Field(default=...)


async def main() -> None:
    settings = Settings()
    access_token = settings.client_access_token.get_secret_value()
    openai_api_key = settings.openai_api_key.get_secret_value()

    client = AsyncOpenAI(api_key=openai_api_key)

    response = await client.responses.create(
        model="gpt-5.1",
        tools=[
            {
                "type": "mcp",
                "server_label": "webquest_mcp",
                "server_url": settings.client_url,
                "require_approval": "never",
                "headers": {"Authorization": f"Bearer {access_token}"},
            },
        ],
        input="Summarize the latest video from TLDR News Global.",
    )

    print(response.output_text)


if __name__ == "__main__":
    asyncio.run(main())
