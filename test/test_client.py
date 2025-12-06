import asyncio

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    access_token: SecretStr = Field(default=...)
    server_url: str = Field(default="http://127.0.0.1:8000/mcp")


async def main() -> None:
    load_dotenv()

    settings = Settings()
    access_token = settings.access_token.get_secret_value()

    openai_client = AsyncOpenAI()

    response = await openai_client.responses.create(
        model="gpt-5.1",
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
