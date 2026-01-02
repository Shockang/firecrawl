"""
Browser-based scraping example.

This example shows how to use Playwright for JavaScript-rendered pages.
"""

import asyncio
from firecrawl import FirecrawlScraper, ScrapeOptions, EngineType


async def main():
    """Scrape a JavaScript-rendered page using Playwright."""
    # Initialize scraper with Playwright engine
    async with FirecrawlScraper(engine=EngineType.PLAYWRIGHT) as scraper:
        # Scrape with screenshot
        options = ScrapeOptions(
            screenshot=True,
            wait_for=2000,  # Wait 2 seconds for JS to execute
        )

        result = await scraper.scrape("https://example.com", options)

        if result.success:
            print("Successfully scraped with browser!")
            print(f"URL: {result.url}")
            print(f"Status: {result.status_code}")

            if result.markdown:
                print(f"\nMarkdown:\n{result.markdown[:500]}...")

            if result.screenshot:
                print(f"\nScreenshot captured (base64 length: {len(result.screenshot)})")
        else:
            print(f"Error: {result.error}")


if __name__ == "__main__":
    asyncio.run(main())
