"""
Basic scraping example.

This example shows how to scrape a single URL.
"""

import asyncio
from firecrawl import FirecrawlScraper


async def main():
    """Scrape a single URL and print the markdown content."""
    async with FirecrawlScraper() as scraper:
        # Simple scrape
        result = await scraper.scrape("https://example.com")

        if result.success:
            print("Success!")
            print(f"URL: {result.url}")
            print(f"Status Code: {result.status_code}")
            print(f"\nMarkdown Content:\n{result.markdown}")
        else:
            print(f"Error: {result.error}")


if __name__ == "__main__":
    asyncio.run(main())
