"""
Command-line interface for Firecrawl Standalone.
"""

import asyncio
import sys
import argparse
import logging
from pathlib import Path
from typing import Optional

from . import FirecrawlScraper, WebCrawler
from .types import ScrapeOptions, CrawlOptions, EngineType

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def scrape_command(args: argparse.Namespace):
    """Handle the scrape command."""
    options = ScrapeOptions(
        formats=[f.strip() for f in args.formats.split(",")] if args.formats else ["markdown"],
        screenshot=args.screenshot,
        timeout=args.timeout,
        only_main_content=not args.full_page,
        engine=EngineType.PLAYWRIGHT if args.browser else EngineType.HTTP,
    )

    async with FirecrawlScraper() as scraper:
        result = await scraper.scrape(args.url, options)

        if not result.success:
            print(f"Error: {result.error}", file=sys.stderr)
            sys.exit(1)

        # Output the result
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            if result.markdown:
                output_path.write_text(result.markdown)
                print(f"Markdown saved to {args.output}")
            elif result.raw_html:
                output_path.write_text(result.raw_html)
                print(f"HTML saved to {args.output}")
        else:
            # Print to stdout
            if result.markdown:
                print(result.markdown)
            elif result.raw_html:
                print(result.raw_html[:500] + "...")


async def crawl_command(args: argparse.Namespace):
    """Handle the crawl command."""
    scrape_options = ScrapeOptions(
        engine=EngineType.PLAYWRIGHT if args.browser else EngineType.HTTP,
    )

    options = CrawlOptions(
        max_pages=args.max_pages,
        max_depth=args.max_depth,
        scrape_options=scrape_options,
    )

    crawler = WebCrawler(default_options=options)

    try:
        results = await crawler.crawl_all(args.url, options)

        if args.output:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)

            for i, result in enumerate(results):
                if result.markdown:
                    filename = f"{i}_{hash(result.url) % 10000}.md"
                    output_path = output_dir / filename
                    output_path.write_text(result.markdown)
                    print(f"Saved {result.url} to {output_path}")
        else:
            for result in results:
                print(f"\n{'='*80}")
                print(f"URL: {result.url}")
                print(f"Status: {result.status_code}")
                if result.markdown:
                    preview = result.markdown[:200]
                    print(f"Preview: {preview}...")

        print(f"\nTotal pages scraped: {len(results)}")

    finally:
        await crawler.close()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Firecrawl Standalone - Web scraping tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape a single URL
  firecrawl scrape https://example.com

  # Scrape with options
  firecrawl scrape https://example.com --browser --screenshot --output result.md

  # Crawl a website
  firecrawl crawl https://example.com --max-pages 10 --output ./output

  # Crawl with depth limit
  firecrawl crawl https://example.com --max-depth 3 --max-pages 50
        """
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Scrape command
    scrape_parser = subparsers.add_parser(
        "scrape",
        help="Scrape a single URL"
    )
    scrape_parser.add_argument(
        "url",
        help="URL to scrape"
    )
    scrape_parser.add_argument(
        "-o", "--output",
        help="Output file path"
    )
    scrape_parser.add_argument(
        "-f", "--formats",
        default="markdown",
        help="Output formats (comma-separated: markdown,html,screenshot)"
    )
    scrape_parser.add_argument(
        "--browser",
        action="store_true",
        help="Use browser engine (Playwright) instead of HTTP"
    )
    scrape_parser.add_argument(
        "--screenshot",
        action="store_true",
        help="Capture screenshot"
    )
    scrape_parser.add_argument(
        "--timeout",
        type=int,
        default=30000,
        help="Timeout in milliseconds (default: 30000)"
    )
    scrape_parser.add_argument(
        "--full-page",
        action="store_true",
        help="Include full page, not just main content"
    )

    # Crawl command
    crawl_parser = subparsers.add_parser(
        "crawl",
        help="Crawl multiple pages"
    )
    crawl_parser.add_argument(
        "url",
        help="Starting URL"
    )
    crawl_parser.add_argument(
        "-o", "--output",
        help="Output directory for scraped pages"
    )
    crawl_parser.add_argument(
        "--max-pages",
        type=int,
        default=10,
        help="Maximum number of pages to crawl (default: 10)"
    )
    crawl_parser.add_argument(
        "--max-depth",
        type=int,
        default=2,
        help="Maximum crawl depth (default: 2)"
    )
    crawl_parser.add_argument(
        "--browser",
        action="store_true",
        help="Use browser engine (Playwright) instead of HTTP"
    )

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "scrape":
        asyncio.run(scrape_command(args))
    elif args.command == "crawl":
        asyncio.run(crawl_command(args))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
