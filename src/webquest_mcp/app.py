from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from webquest.browsers import Hyperbrowser
from webquest.scrapers.any_article import (
    AnyArticle,
    AnyArticleRequest,
    AnyArticleResponse,
)
from webquest.scrapers.duckduckgo_search import (
    DuckDuckGoSearch,
    DuckDuckGoSearchRequest,
    DuckDuckGoSearchResponse,
)
from webquest.scrapers.google_news_search import (
    GoogleNewsSearch,
    GoogleNewsSearchRequest,
    GoogleNewsSearchResponse,
)
from webquest.scrapers.youtube_search import (
    YouTubeSearch,
    YouTubeSearchRequest,
    YouTubeSearchResponse,
)
from webquest.scrapers.youtube_transcript import (
    YouTubeTranscript,
    YouTubeTranscriptRequest,
    YouTubeTranscriptResponse,
)


@dataclass
class AppContext:
    any_article: AnyArticle
    duckduckgo_search: DuckDuckGoSearch
    google_news_search: GoogleNewsSearch
    youtube_search: YouTubeSearch
    youtube_transcript: YouTubeTranscript


@asynccontextmanager
async def app_lifespan(_: FastMCP) -> AsyncIterator[AppContext]:
    browser = Hyperbrowser()
    any_article = AnyArticle(browser=browser)
    duckduckgo_search = DuckDuckGoSearch(browser=browser)
    google_news_search = GoogleNewsSearch(browser=browser)
    youtube_search = YouTubeSearch(browser=browser)
    youtube_transcript = YouTubeTranscript(browser=browser)
    try:
        yield AppContext(
            any_article=any_article,
            duckduckgo_search=duckduckgo_search,
            google_news_search=google_news_search,
            youtube_search=youtube_search,
            youtube_transcript=youtube_transcript,
        )
    finally:
        pass


mcp = FastMCP("WebQuest MCP", lifespan=app_lifespan)


@mcp.tool()
async def any_article(
    request: AnyArticleRequest,
    ctx: Context[ServerSession, AppContext],
) -> AnyArticleResponse:
    """Get the content of an article given its URL."""
    scraper = ctx.request_context.lifespan_context.any_article
    response = await scraper.run(request)
    return response


@mcp.tool()
async def duckduckgo_search(
    request: DuckDuckGoSearchRequest,
    ctx: Context[ServerSession, AppContext],
) -> DuckDuckGoSearchResponse:
    """Search the web using DuckDuckGo given a query."""
    scraper = ctx.request_context.lifespan_context.duckduckgo_search
    response = await scraper.run(request)
    return response


@mcp.tool()
async def google_news_search(
    request: GoogleNewsSearchRequest,
    ctx: Context[ServerSession, AppContext],
) -> GoogleNewsSearchResponse:
    """Search for news articles using Google News given a query."""
    scraper = ctx.request_context.lifespan_context.google_news_search
    response = await scraper.run(request)
    return response


@mcp.tool()
async def youtube_search(
    request: YouTubeSearchRequest,
    ctx: Context[ServerSession, AppContext],
) -> YouTubeSearchResponse:
    """Search for YouTube videos, channels, posts, and shorts given a query."""
    scraper = ctx.request_context.lifespan_context.youtube_search
    response = await scraper.run(request)
    return response


@mcp.tool()
async def youtube_transcript(
    request: YouTubeTranscriptRequest,
    ctx: Context[ServerSession, AppContext],
) -> YouTubeTranscriptResponse:
    """Get the transcript of a YouTube video given its ID."""
    scraper = ctx.request_context.lifespan_context.youtube_transcript
    response = await scraper.run(request)
    return response
