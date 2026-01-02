"""
Multi-page website crawler.

This module provides functionality to crawl multiple pages of a website.
"""

import asyncio
import logging
from typing import List, Set, Optional, AsyncIterator
from urllib.parse import urljoin

from .scraper import FirecrawlScraper
from .types import ScrapeResult, CrawlOptions
from .utils.robots import RobotsChecker
from .utils.filters import URLFilter
from .parsers.markdown import HTMLToMarkdown

logger = logging.getLogger(__name__)


class WebCrawler:
    """
    Crawl multiple pages of a website.

    This class handles crawling multiple pages, respecting robots.txt,
    filtering URLs, and managing the crawl queue.

    Example:
        ```python
        crawler = WebCrawler()

        # Crawl a website
        async for result in crawler.crawl("https://example.com", max_pages=10):
            print(f"Scraped: {result.url}")
            print(result.markdown[:100])

        # Or get all results at once
        results = await crawler.crawl_all("https://example.com", max_pages=10)
        ```
    """

    def __init__(
        self,
        default_options: Optional[CrawlOptions] = None
    ):
        """
        Initialize the crawler.

        Args:
            default_options: Default options for crawling
        """
        self.default_options = default_options or CrawlOptions()
        self.scraper: Optional[FirecrawlScraper] = None
        self.markdown_parser = HTMLToMarkdown()

    async def crawl(
        self,
        url: str,
        options: Optional[CrawlOptions] = None
    ) -> AsyncIterator[ScrapeResult]:
        """
        Crawl a website asynchronously.

        Args:
            url: The starting URL
            options: Options for this crawl

        Yields:
            ScrapeResult for each page as it's scraped
        """
        opts = options or self.default_options

        # Initialize components
        self.scraper = FirecrawlScraper(
            default_options=opts.scrape_options
        )

        # Initialize URL filter
        url_filter = URLFilter(
            base_url=url,
            include_patterns=opts.include_patterns,
            exclude_patterns=opts.exclude_patterns,
            allow_backwards=opts.allow_backwards,
            max_depth=opts.max_depth
        )

        # Initialize robots checker
        robots_checker = RobotsChecker(url)
        await robots_checker.fetch()

        # Crawl state
        visited: Set[str] = set()
        queue: asyncio.Queue[str] = asyncio.Queue()
        await queue.put(url_filter.normalize_url(url))

        pages_scraped = 0

        try:
            while not queue.empty() and pages_scraped < opts.max_pages:
                current_url = await queue.get()

                if current_url in visited:
                    continue

                # Check if allowed by robots.txt
                if not robots_checker.is_allowed(current_url):
                    logger.info(f"Skipped {current_url} (disallowed by robots.txt)")
                    continue

                # Check if URL passes filters
                if not url_filter.should_crawl(current_url):
                    logger.debug(f"Skipped {current_url} (filtered)")
                    continue

                # Mark as visited
                visited.add(current_url)

                # Scrape the page
                logger.info(f"Scraping {current_url}")
                result = await self.scraper.scrape(current_url)

                if not result.success:
                    logger.warning(f"Failed to scrape {current_url}: {result.error}")
                    continue

                pages_scraped += 1
                yield result

                # Extract links from the page
                if result.raw_html:
                    links = self.markdown_parser.extract_links(
                        result.raw_html,
                        base_url=result.url
                    )

                    # Add new links to queue
                    for link in links:
                        normalized = url_filter.normalize_url(link)
                        if normalized not in visited:
                            try:
                                queue.put_nowait(normalized)
                            except asyncio.QueueFull:
                                break

        finally:
            if self.scraper:
                await self.scraper.close()

    async def crawl_all(
        self,
        url: str,
        options: Optional[CrawlOptions] = None
    ) -> List[ScrapeResult]:
        """
        Crawl a website and return all results.

        Args:
            url: The starting URL
            options: Options for this crawl

        Returns:
            List of ScrapeResults
        """
        results = []
        async for result in self.crawl(url, options):
            results.append(result)
        return results

    async def close(self):
        """
        Close the crawler and release resources.

        Always call this when done crawling.
        """
        if self.scraper:
            await self.scraper.close()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
