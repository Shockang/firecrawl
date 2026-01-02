# Firecrawl - Standalone Python Web Scraper

A standalone Python web scraper for easy integration into existing projects.

This package extracts core scraping functionality from the Firecrawl project, allowing you to scrape web pages and crawl websites without needing any external API server or dependencies.

## Features

- **Simple Scraping**: Scrape single URLs with just a few lines of code
- **Multiple Engines**: Choose between fast HTTP or powerful Playwright browser engine
- **Markdown Output**: Clean markdown extraction with content filtering
- **Website Crawling**: Crawl multiple pages with depth control and URL filtering
- **Robots.txt Respect**: Automatically respects robots.txt files
- **Async/First**: Built with asyncio for efficient concurrent operations

## Installation

```bash
# Install from source
cd firecrawl-standalone
pip install -e .

# Or install dependencies manually
pip install -r requirements.txt

# If using Playwright engine, install browsers
playwright install chromium
```

## Quick Start

### Scraping a Single URL

```python
import asyncio
from firecrawl import FirecrawlScraper

async def main():
    async with FirecrawlScraper() as scraper:
        result = await scraper.scrape("https://example.com")

        if result.success:
            print(result.markdown)
        else:
            print(f"Error: {result.error}")

asyncio.run(main())
```

### Crawling a Website

```python
import asyncio
from firecrawl import FirecrawlScraper

async def main():
    async with FirecrawlScraper() as scraper:
        async for result in scraper.crawl(
            "https://example.com",
            max_pages=10,
            max_depth=2
        ):
            print(f"Scraped: {result.url}")
            print(result.markdown[:100] + "...")

asyncio.run(main())
```

## CLI Usage

```bash
# Scrape a single URL
firecrawl scrape https://example.com

# Crawl a website
firecrawl crawl https://example.com --max-pages 10 --output ./output
```

## Documentation

See [firecrawl-standalone/README.md](firecrawl-standalone/README.md) for full documentation.

## Project Structure

```
firecrawl/
├── firecrawl-standalone/          # Core standalone Python package
│   ├── firecrawl/                 # Main package code
│   ├── examples/                  # Usage examples
│   ├── tests/                     # Test suite
│   └── README.md                  # Package documentation
├── LICENSE                        # License file
├── CLAUDE.md                      # AI assistant instructions
└── README.md                      # This file
```

## License

Apache License 2.0 - See [LICENSE](LICENSE) for details.
