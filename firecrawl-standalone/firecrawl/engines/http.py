"""
HTTP-based scraping engine using httpx.

This is a lightweight, fast engine that fetches pages using HTTP requests.
It doesn't execute JavaScript but is much faster than browser-based engines.
"""

import logging
from typing import Optional
import httpx
from urllib.parse import urlparse

from .base import BaseEngine
from ..types import ScrapeOptions, ScrapeResult
from ..parsers.markdown import HTMLToMarkdown

logger = logging.getLogger(__name__)


class HTTPEngine(BaseEngine):
    """
    HTTP-based scraping engine using httpx.

    Fast and lightweight but doesn't execute JavaScript.
    Best for static content or when speed is critical.
    """

    def __init__(self, options: Optional[ScrapeOptions] = None):
        super().__init__(options)
        self.client: Optional[httpx.AsyncClient] = None
        self.markdown_converter = HTMLToMarkdown()

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self.client is None:
            timeout = httpx.Timeout(
                max(self.default_options.timeout / 1000.0, 5.0),
                connect=10.0
            )
            self.client = httpx.AsyncClient(
                timeout=timeout,
                follow_redirects=True,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; Firecrawl/1.0; +https://firecrawl.dev)",
                }
            )
        return self.client

    async def scrape(
        self,
        url: str,
        options: Optional[ScrapeOptions] = None
    ) -> ScrapeResult:
        """
        Scrape a URL using HTTP request.

        Args:
            url: The URL to scrape
            options: Options for this specific scrape

        Returns:
            ScrapeResult with the scraped content
        """
        opts = self._merge_options(options)

        try:
            # Validate URL
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return ScrapeResult(
                    url=url,
                    status_code=400,
                    error=f"Invalid URL: {url}"
                )

            client = await self._get_client()

            # Prepare headers
            headers = {}
            if opts.headers:
                headers.update(opts.headers)

            # Fetch the page
            logger.info(f"Fetching URL via HTTP: {url}")
            response = await client.get(
                url,
                headers=headers if headers else None
            )

            raw_html = response.text
            markdown = None
            screenshot = None

            # Convert to markdown if requested
            if any(f.value in ["markdown", "screenshot"] for f in opts.formats):
                markdown = await self.markdown_converter.convert(
                    raw_html,
                    url,
                    only_main_content=opts.only_main_content
                )

            return ScrapeResult(
                url=str(response.url),
                markdown=markdown,
                raw_html=raw_html,
                screenshot=screenshot,
                status_code=response.status_code,
                metadata={
                    "engine": "http",
                    "content_type": response.headers.get("content-type", ""),
                    "content_length": len(raw_html),
                }
            )

        except httpx.TimeoutException:
            logger.error(f"Timeout while scraping {url}")
            return ScrapeResult(
                url=url,
                status_code=408,
                error=f"Request timeout after {opts.timeout}ms"
            )
        except httpx.HTTPError as e:
            logger.error(f"HTTP error while scraping {url}: {e}")
            return ScrapeResult(
                url=url,
                status_code=getattr(e.response, "status_code", 500),
                error=str(e)
            )
        except Exception as e:
            logger.error(f"Unexpected error while scraping {url}: {e}")
            return ScrapeResult(
                url=url,
                status_code=500,
                error=f"Unexpected error: {str(e)}"
            )

    async def close(self):
        """Close the HTTP client."""
        if self.client:
            await self.client.aclose()
            self.client = None
