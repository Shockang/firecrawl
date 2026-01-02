"""
Main Firecrawl scraper class.

This is the primary interface for scraping web pages.
"""

import logging
from typing import Optional, List

from .types import ScrapeOptions, ScrapeResult, EngineType
from .engines.base import BaseEngine
from .engines.http import HTTPEngine
from .engines.playwright import PlaywrightEngine

logger = logging.getLogger(__name__)


class FirecrawlScraper:
    """
    Main scraper class for Firecrawl Standalone.

    This class provides a simple interface for scraping web pages using
    different engines (HTTP, Playwright).

    Example:
        ```python
        scraper = FirecrawlScraper()

        # Simple scrape
        result = await scraper.scrape("https://example.com")
        print(result.markdown)

        # With options
        result = await scraper.scrape(
            "https://example.com",
            formats=["markdown", "html"],
            screenshot=True
        )

        # Clean up
        await scraper.close()
        ```
    """

    def __init__(
        self,
        engine: EngineType = EngineType.HTTP,
        default_options: Optional[ScrapeOptions] = None
    ):
        """
        Initialize the scraper.

        Args:
            engine: Which engine to use (http or playwright)
            default_options: Default options for all scrapes
        """
        self.engine_type = engine
        self.default_options = default_options or ScrapeOptions()
        self.engine: Optional[BaseEngine] = None
        self._initialize_engine()

    def _initialize_engine(self):
        """Initialize the selected engine."""
        if self.engine_type == EngineType.PLAYWRIGHT:
            self.engine = PlaywrightEngine(self.default_options)
        else:
            self.engine = HTTPEngine(self.default_options)

    async def scrape(
        self,
        url: str,
        options: Optional[ScrapeOptions] = None
    ) -> ScrapeResult:
        """
        Scrape a URL and return the result.

        Args:
            url: The URL to scrape
            options: Options for this specific scrape

        Returns:
            ScrapeResult with the scraped content
        """
        if not self.engine:
            self._initialize_engine()

        return await self.engine.scrape(url, options)

    async def scrape_multiple(
        self,
        urls: List[str],
        options: Optional[ScrapeOptions] = None
    ) -> List[ScrapeResult]:
        """
        Scrape multiple URLs concurrently.

        Args:
            urls: List of URLs to scrape
            options: Options to use for all scrapes

        Returns:
            List of ScrapeResults in the same order as URLs
        """
        import asyncio

        if not self.engine:
            self._initialize_engine()

        tasks = [self.engine.scrape(url, options) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert any exceptions to error results
        final_results = []
        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                final_results.append(ScrapeResult(
                    url=url,
                    status_code=500,
                    error=str(result)
                ))
            else:
                final_results.append(result)

        return final_results

    async def close(self):
        """
        Close the scraper and release resources.

        Always call this when done scraping to properly clean up.
        """
        if self.engine:
            if hasattr(self.engine, 'close'):
                await self.engine.close()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
