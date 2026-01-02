"""
Firecrawl Standalone - A standalone web scraper for easy integration into Python projects.

This package provides core scraping functionality extracted from the Firecrawl project,
allowing you to scrape web pages and crawl websites without needing the full API server.
"""

from .scraper import FirecrawlScraper
from .crawler import WebCrawler
from .types import ScrapeResult, ScrapeOptions, CrawlOptions

__version__ = "0.1.0"
__all__ = [
    "FirecrawlScraper",
    "WebCrawler",
    "ScrapeResult",
    "ScrapeOptions",
    "CrawlOptions",
]
