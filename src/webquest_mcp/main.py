from dotenv import load_dotenv

from webquest_mcp.app import mcp


def main() -> None:
    load_dotenv()
    mcp.run(transport="streamable-http")
