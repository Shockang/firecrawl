"""
Basic tests for the Firecrawl Standalone scraper.
"""

import pytest
import asyncio
from firecrawl import FirecrawlScraper, ScrapeOptions, EngineType


@pytest.mark.asyncio
async def test_basic_scrape():
    """Test basic scraping functionality."""
    scraper = FirecrawlScraper()

    try:
        result = await scraper.scrape("https://example.com")

        assert result.success
        assert result.url == "https://example.com"
        assert result.markdown is not None
        assert len(result.markdown) > 0
        assert result.status_code == 200

    finally:
        await scraper.close()


@pytest.mark.asyncio
async def test_scrape_multiple():
    """Test scraping multiple URLs."""
    scraper = FirecrawlScraper()

    try:
        urls = [
            "https://example.com",
            "https://example.com",
        ]

        results = await scraper.scrape_multiple(urls)

        assert len(results) == 2
        assert all(r.success for r in results)

    finally:
        await scraper.close()


@pytest.mark.asyncio
async def test_context_manager():
    """Test using scraper as context manager."""
    async with FirecrawlScraper() as scraper:
        result = await scraper.scrape("https://example.com")
        assert result.success


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
