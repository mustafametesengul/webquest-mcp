import asyncio

from openai import AsyncOpenAI
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    access_token: SecretStr = Field(default=...)
    server_url: str = Field(default=...)


async def main() -> None:
    settings = Settings()
    access_token = settings.access_token.get_secret_value()

    openai_client = AsyncOpenAI()

    response = await openai_client.responses.create(
        model="gpt-5.1",
        max_output_tokens=10000,
        max_tool_calls=5,
        tools=[
            {
                "type": "mcp",
                "server_label": "webquest_mcp",
                "server_url": settings.server_url,
                "require_approval": "never",
                "headers": {"Authorization": f"Bearer {access_token}"},
            },
        ],
        input="Summarize the latest video from TLDR News Global.",
    )

    print(response.output_text)


if __name__ == "__main__":
    asyncio.run(main())
