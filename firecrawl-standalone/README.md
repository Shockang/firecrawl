# Firecrawl Standalone

A standalone Python web scraper for easy integration into existing projects.

This package extracts the core scraping functionality from the Firecrawl project, allowing you to scrape web pages and crawl websites without needing the full API server.

## Features

- **Simple Scraping**: Scrape single URLs with just a few lines of code
- **Multiple Engines**: Choose between fast HTTP or powerful Playwright browser engine
- **Markdown Output**: Clean markdown extraction with content filtering
- **Website Crawling**: Crawl multiple pages with depth control and URL filtering
- **Robots.txt Respect**: Automatically respects robots.txt files
- **Screenshot Capture**: Optional screenshot capture with Playwright engine
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
from firecrawl import WebCrawler, CrawlOptions

async def main():
    crawler = WebCrawler()

    options = CrawlOptions(
        max_pages=10,
        max_depth=2,
    )

    async for result in crawler.crawl("https://example.com", options):
        print(f"Scraped: {result.url}")
        print(f"Content: {result.markdown[:100]}...")

    await crawler.close()

asyncio.run(main())
```

### Using the CLI

```bash
# Scrape a single URL
firecrawl scrape https://example.com

# Scrape with browser and screenshot
firecrawl scrape https://example.com --browser --screenshot

# Crawl a website
firecrawl crawl https://example.com --max-pages 10 --output ./output

# See all options
firecrawl scrape --help
firecrawl crawl --help
```

## Architecture

### Core Components

- **FirecrawlScraper**: Main scraper class for single-page scraping
- **WebCrawler**: Multi-page crawler with queue management
- **Engines**:
  - `HTTPEngine`: Fast HTTP-based scraping (no JavaScript)
  - `PlaywrightEngine`: Browser-based scraping with JavaScript support
- **Parsers**:
  - `HTMLToMarkdown`: Converts HTML to clean markdown
- **Utils**:
  - `RobotsChecker`: Fetches and respects robots.txt
  - `URLFilter`: Filters URLs during crawling

### Design Decisions

1. **Engine Selection**:
   - Default: HTTP engine (fast, lightweight)
   - For JS sites: Playwright engine (slower, but renders JavaScript)

2. **Markdown Conversion**:
   - Uses `markdownify` library
   - Removes non-content elements (nav, footer, etc.)
   - Preserves links and structure

3. **Crawling Strategy**:
   - BFS (breadth-first search) with async queue
   - Deduplication via visited set
   - Respects robots.txt
   - URL filtering by pattern, domain, and depth

## Advanced Usage

### Custom Scraping Options

```python
from firecrawl import FirecrawlScraper, ScrapeOptions, EngineType

scraper = FirecrawlScraper()

options = ScrapeOptions(
    engine=EngineType.PLAYWRIGHT,  # Use browser engine
    screenshot=True,                # Capture screenshot
    wait_for=2000,                  # Wait 2 seconds for JS
    only_main_content=True,         # Extract only main content
    timeout=60000,                  # 60 second timeout
)

result = await scraper.scrape("https://example.com", options)
```

### Custom Crawl Options

```python
from firecrawl import WebCrawler, CrawlOptions

crawler = WebCrawler()

options = CrawlOptions(
    max_pages=50,                   # Maximum pages to crawl
    max_depth=3,                    # Maximum link depth
    include_patterns=[r"/blog/.*"], # Only include blog posts
    exclude_patterns=[r"/admin/.*"],# Exclude admin pages
    allow_backwards=False,          # Don't crawl parent directories
)

results = await crawler.crawl_all("https://example.com", options)
```

### Batch Scraping

```python
from firecrawl import FirecrawlScraper

scraper = FirecrawlScraper()

urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
]

# Scrape multiple URLs concurrently
results = await scraper.scrape_multiple(urls)

for result in results:
    print(f"{result.url}: {len(result.markdown)} chars")
```

## Project Structure

```
firecrawl-standalone/
├── firecrawl/
│   ├── __init__.py       # Package initialization
│   ├── scraper.py        # Main scraper class
│   ├── crawler.py        # Multi-page crawler
│   ├── types.py          # Type definitions
│   ├── cli.py            # Command-line interface
│   ├── engines/          # Scraping engines
│   │   ├── base.py       # Base engine interface
│   │   ├── http.py       # HTTP engine
│   │   └── playwright.py # Playwright engine
│   ├── parsers/          # Content parsers
│   │   └── markdown.py   # HTML to markdown
│   └── utils/            # Utilities
│       ├── robots.py     # Robots.txt handling
│       └── filters.py    # URL filtering
├── examples/             # Usage examples
├── tests/                # Tests
├── pyproject.toml        # Package configuration
└── README.md            # This file
```

## API Reference

### FirecrawlScraper

Main scraper class for single-page scraping.

**Methods:**
- `async scrape(url: str, options: ScrapeOptions = None) -> ScrapeResult`
- `async scrape_multiple(urls: List[str], options: ScrapeOptions = None) -> List[ScrapeResult]`
- `async close()` - Clean up resources

### WebCrawler

Multi-page crawler with queue management.

**Methods:**
- `async crawl(url: str, options: CrawlOptions = None) -> AsyncIterator[ScrapeResult]`
- `async crawl_all(url: str, options: CrawlOptions = None) -> List[ScrapeResult]`
- `async close()` - Clean up resources

### ScrapeResult

Result from scraping a URL.

**Properties:**
- `url: str` - The URL that was scraped
- `markdown: Optional[str]` - Content in markdown format
- `raw_html: Optional[str]` - Raw HTML content
- `screenshot: Optional[str]` - Base64 encoded screenshot
- `status_code: int` - HTTP status code
- `error: Optional[str]` - Error message if failed
- `success: bool` - Check if scrape was successful
- `metadata: Dict[str, Any]` - Additional metadata

## Differences from Full Firecrawl

This standalone version provides core scraping functionality but excludes:

- No API server (direct Python integration)
- No authentication/rate limiting
- No queue system (BullMQ)
- No LLM extraction (can be added separately)
- No search integration
- No change tracking
- No branding profiles

These features can be added as needed or integrated with external services.

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
black firecrawl/
ruff check firecrawl/

# Type checking
mypy firecrawl/
```

## Contributing

When contributing to this package:

1. Keep it standalone - no dependencies on the full Firecrawl API
2. Use type hints for all public APIs
3. Add tests for new features
4. Update documentation for any API changes

## License

MIT License - See LICENSE file for details

## Related Projects

- [Firecrawl](https://github.com/mendableai/firecrawl) - Full scraping platform
- [Firecrawl Python SDK](../apps/python-sdk/) - Client SDK for Firecrawl API
