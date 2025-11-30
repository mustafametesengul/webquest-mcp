import asyncio
import os

from dotenv import load_dotenv
from fastmcp import Client


async def main():
    load_dotenv()

    access_token = os.getenv("ACCESS_TOKEN")

    async with Client(
        "http://127.0.0.1:8000/mcp",
        auth=access_token,
    ) as client:
        await client.ping()


if __name__ == "__main__":
    asyncio.run(main())
