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

## Migration Notes

### For API Server Users

If you were using the Firecrawl API server, you have two options:

1. **Use the standalone Python package** (recommended)
   - No server needed
   - Direct Python integration
   - See firecrawl-standalone/ for usage guide

2. **Use the archived version**
   - Original API server is preserved in the `archive/original-api-implementation` branch
   - Can checkout that branch if needed: `git checkout archive/original-api-implementation`

### For SDK Users

If you were using the Python/Node/Rust SDKs:

- The standalone package replaces the need for SDKs
- Direct Python integration instead of API calls
- See examples in firecrawl-standalone/examples/

## Benefits

- **Simple**: Only one codebase to understand
- **Focused**: Clear project goal
- **Small**: Minimal repository size
- **Fast**: No API server overhead
- **Easy**: Direct Python integration
- **Lightweight**: Minimal dependencies
- **Flexible**: Use as library or CLI tool
- **No Server**: Run anywhere without infrastructure

## License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

## Contributing

We love contributions! Please read our contributing guide before submitting a pull request.

_It is the sole responsibility of the end users to respect websites' policies when scraping and crawling with Firecrawl. Users are advised to adhere to the applicable privacy policies and terms of use of the websites prior to initiating any scraping activities. By default, Firecrawl respects the directives specified in the websites' robots.txt files when crawling. By utilizing Firecrawl, you expressly agree to comply with these conditions._
