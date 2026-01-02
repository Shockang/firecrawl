"""
Playwright-based scraping engine.

This engine uses Playwright to render pages in a real browser,
allowing it to handle JavaScript-rendered content.
"""

import logging
from typing import Optional
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
import base64

from .base import BaseEngine
from ..types import ScrapeOptions, ScrapeResult, EngineType
from ..parsers.markdown import HTMLToMarkdown

logger = logging.getLogger(__name__)


class PlaywrightEngine(BaseEngine):
    """
    Playwright-based scraping engine.

    Uses a headless browser to render pages, enabling JavaScript execution
    and screenshot capture. Slower than HTTP but more powerful.
    """

    def __init__(self, options: Optional[ScrapeOptions] = None):
        super().__init__(options)
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.markdown_converter = HTMLToMarkdown()

    async def _get_browser(self) -> Browser:
        """Get or create browser instance."""
        if self.browser is None:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=True)
        return self.browser

    async def _get_context(self) -> BrowserContext:
        """Get or create browser context."""
        if self.context is None:
            browser = await self._get_browser()
            self.context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (compatible; Firecrawl/1.0; +https://firecrawl.dev)"
            )
        return self.context

    async def scrape(
        self,
        url: str,
        options: Optional[ScrapeOptions] = None
    ) -> ScrapeResult:
        """
        Scrape a URL using Playwright browser.

        Args:
            url: The URL to scrape
            options: Options for this specific scrape

        Returns:
            ScrapeResult with the scraped content
        """
        opts = self._merge_options(options)

        try:
            context = await self._get_context()
            page = await context.new_page()

            try:
                # Set timeout
                timeout = opts.timeout

                # Navigate to URL
                logger.info(f"Fetching URL via Playwright: {url}")
                await page.goto(url, timeout=timeout, wait_until="domcontentloaded")

                # Wait if specified
                if opts.wait_for:
                    logger.debug(f"Waiting {opts.wait_for}ms after page load")
                    await page.wait_for_timeout(opts.wait_for)

                # Get content
                raw_html = await page.content()

                # Screenshot if requested
                screenshot = None
                if opts.screenshot:
                    screenshot_bytes = await page.screenshot(
                        full_page=False,
                        type="png"
                    )
                    screenshot = base64.b64encode(screenshot_bytes).decode("utf-8")

                # Convert to markdown if requested
                markdown = None
                if any(f.value in ["markdown", "screenshot"] for f in opts.formats):
                    markdown = await self.markdown_converter.convert(
                        raw_html,
                        url,
                        only_main_content=opts.only_main_content
                    )

                return ScrapeResult(
                    url=url,
                    markdown=markdown,
                    raw_html=raw_html,
                    screenshot=screenshot,
                    status_code=200,
                    metadata={
                        "engine": "playwright",
                        "title": await page.title(),
                    }
                )

            finally:
                await page.close()

        except Exception as e:
            logger.error(f"Error scraping {url} with Playwright: {e}")
            return ScrapeResult(
                url=url,
                status_code=500,
                error=f"Playwright error: {str(e)}"
            )

    async def close(self):
        """Close the browser and context."""
        if self.context:
            await self.context.close()
            self.context = None
        if self.browser:
            await self.browser.close()
            self.browser = None
