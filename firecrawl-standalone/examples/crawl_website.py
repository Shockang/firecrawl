"""
Website crawling example.

This example shows how to crawl multiple pages of a website.
"""

import asyncio
from firecrawl import WebCrawler, CrawlOptions


async def main():
    """Crawl a website and print information about each page."""
    crawler = WebCrawler()

    # Crawl options
    options = CrawlOptions(
        max_pages=10,
        max_depth=2,
    )

    try:
        # Crawl the website
        async for result in crawler.crawl("https://example.com", options):
            if result.success:
                print(f"\n{'='*80}")
                print(f"URL: {result.url}")
                print(f"Status: {result.status_code}")
                if result.markdown:
                    print(f"Content Length: {len(result.markdown)} characters")
                    print(f"Preview: {result.markdown[:150]}...")
            else:
                print(f"Failed to scrape: {result.url}")
                print(f"Error: {result.error}")

    finally:
        await crawler.close()


if __name__ == "__main__":
    asyncio.run(main())
