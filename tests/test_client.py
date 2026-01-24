import asyncio

from openai import AsyncOpenAI
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: SecretStr = Field(default=...)
    test_access_token: SecretStr = Field(default=...)
    test_server_url: str = Field(default=...)


async def test_client() -> None:
    settings = Settings()

    access_token = settings.test_access_token.get_secret_value()
    openai_client = AsyncOpenAI(api_key=settings.openai_api_key.get_secret_value())

    print(f"Connecting to MCP server at {settings.test_server_url}")
    response = await openai_client.responses.create(
        model="gpt-5.2",
        max_output_tokens=10000,
        max_tool_calls=5,
        tools=[
            {
                "type": "mcp",
                "server_label": "webquest_mcp",
                "server_url": settings.test_server_url,
                "require_approval": "never",
                "headers": {"Authorization": f"Bearer {access_token}"},
            },
        ],
        input="Summarize the latest video from TLDR News Global.",
    )

    print(response.output_text)


if __name__ == "__main__":
    asyncio.run(test_client())
