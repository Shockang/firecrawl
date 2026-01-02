# Next Iteration Action Plan

## Understanding the Current Situation

### What Exists
- **Node.js/TypeScript API**: Full scraping backend (~111K lines)
- **Python SDK**: HTTP client wrapper (calls the API, not standalone)
- **Multiple Services**:
  - Go Markdown Service (HTML→Markdown)
  - Playwright Service (browser automation)
  - Fire-engine (custom Rust scraper)

### The Goal
Create **standalone Python scripts** that can be integrated into existing projects WITHOUT requiring the full Node.js API server.

## Recommended Approach: Build Standalone Python Scraper

### Why This is the Right Approach

1. **User's stated goal**: "封装成 python 脚本方便集成到现有工程中" (encapsulate as Python scripts for easy integration)
2. **Remove non-core code**: Doesn't need full API server, auth, queues, etc.
3. **Standalone**: Should work without Node.js dependency

### Implementation Strategy

#### Phase 1: Core Scraper (MVP) - NEXT ITERATION

**File Structure**:
```
firecrawl-standalone/
├── firecrawl/
│   ├── __init__.py
│   ├── scraper.py          # Main scraper class
│   ├── crawler.py          # Multi-page crawler
│   ├── engines/
│   │   ├── __init__.py
│   │   ├── base.py         # Base engine interface
│   │   ├── playwright.py   # Playwright engine
│   │   └── http.py         # Simple HTTP fetch
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── markdown.py     # HTML to Markdown
│   │   └── extractor.py    # Link extraction
│   └── utils/
│       ├── __init__.py
│       ├── robots.py       # robots.txt handling
│       └── filters.py      # URL filtering
├── examples/
│   ├── basic_scrape.py
│   └── crawl_website.py
├── pyproject.toml
└── requirements.txt
```

**Key Features for MVP**:
1. Single URL scraping
2. Markdown output
3. Basic crawler (multi-page)
4. robots.txt respect
5. URL filtering

**Dependencies**:
```txt
playwright>=1.40.0
markdownify>=0.11.6
beautifulsoup4>=4.12.0
httpx>=0.25.0
aiohttp>=3.9.0
pydantic>=2.0.0
```

**Usage Example**:
```python
from firecrawl import FirecrawlScraper

# Simple scrape
scraper = FirecrawlScraper()
result = scraper.scrape("https://example.com")
print(result.markdown)

# With options
result = scraper.scrape(
    "https://example.com",
    formats=["markdown", "html"],
    screenshot=True,
)

# Crawling
crawler = scraper.crawl("https://example.com", max_pages=10)
for page in crawler:
    print(page.url, page.markdown[:100])
```

#### Phase 2: Advanced Features

1. **LLM Extraction**: Use OpenAI API for structured data
2. **Screenshots**: Playwright screenshot capture
3. **Search Integration**: Web search + scraping
4. **Batch Processing**: Multiple URLs concurrently
5. **Change Tracking**: Detect content changes

#### Phase 3: Polish & Integration

1. CLI interface
2. Configuration file support
3. Better error handling
4. Logging
5. Documentation

## Implementation Tasks (Priority Order)

### Task 1: Base Scraper Class
Create the main `FirecrawlScraper` class with:
- URL validation
- Engine selection (playwright vs HTTP)
- Format handling (markdown, HTML, screenshot)
- Error handling

**Reference**: `apps/api/src/scraper/scrapeURL/index.ts`

### Task 2: Playwright Engine
Implement Playwright-based scraping:
- Page loading
- JavaScript execution
- Screenshot capture
- Actions (click, scroll, wait)

**Reference**: `apps/api/src/scraper/scrapeURL/engines/playwright/`

**Python Equivalent**:
```python
from playwright.async_api import async_playwright

async def scrape_with_playwright(url, options):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        html = await page.content()
        screenshot = await page.screenshot() if options.screenshot else None
        await browser.close()
        return {'html': html, 'screenshot': screenshot}
```

### Task 3: Markdown Parser
Convert HTML to clean markdown:
- Use `markdownify` library
- Preserve links
- Handle tables
- Clean unwanted elements

**Reference**: `apps/go-html-to-md-service/`

**Python Implementation**:
```python
from markdownify import markdownify as md
from bs4 import BeautifulSoup

def html_to_markdown(html, options=None):
    soup = BeautifulSoup(html, 'lxml')

    # Remove unwanted elements
    for tag in soup(['script', 'style', 'nav', 'footer']):
        tag.decompose()

    # Convert to markdown
    markdown = md(str(soup))

    return markdown
```

### Task 4: Crawler
Implement multi-page crawling:
- Link discovery
- robots.txt handling
- Depth control
- URL filtering
- Deduplication

**Reference**: `apps/api/src/scraper/WebScraper/crawler.ts`

**Key Logic**:
```python
class WebCrawler:
    def __init__(self, base_url, options):
        self.base_url = base_url
        self.visited = set()
        self.queue = [base_url]
        self.robots = self._fetch_robots_txt()

    async def crawl(self, max_pages=10):
        while self.queue and len(self.visited) < max_pages:
            url = self.queue.pop(0)
            if url in self.visited:
                continue

            if not self._is_allowed(url):
                continue

            result = await self.scraper.scrape(url)
            self.visited.add(url)

            # Extract links
            links = self._extract_links(result.html)
            for link in links:
                if self._should_crawl(link):
                    self.queue.append(link)

            yield result
```

### Task 5: URL Filtering & Utils
Implement:
- robots.txt parser
- URL pattern matching (include/exclude)
- Depth calculation
- Domain filtering

**Reference**: `apps/api/src/scraper/WebScraper/utils/`

### Task 6: Testing
Write tests for:
- Basic scraping
- Markdown output
- Crawling logic
- robots.txt respect
- Error handling

### Task 7: CLI Interface
Create command-line tool:
```bash
# Scrape single URL
firecrawl scrape https://example.com -o output.md

# Crawl website
firecrawl crawl https://example.com --max-pages 10 -o output/

# With options
firecrawl scrape https://example.com --formats markdown,html --screenshot
```

### Task 8: Documentation
Write:
- Installation instructions
- Usage examples
- API reference
- Configuration guide

## Coding Standards

1. **Type Hints**: Use Python 3.10+ type hints
2. **Async First**: Use asyncio for I/O operations
3. **Error Handling**: Clear error messages
4. **Logging**: Structured logging with Python logging module
5. **Configuration**: Pydantic models for config
6. **Testing**: pytest with async support

## Key Decisions for Next Developer

### 1. Scraping Engine Selection
- **Playwright** (Recommended): Best for JS-rendered sites
- **HTTP+BeautifulSoup**: Faster, no JS support
- **Both**: Fallback from HTTP → Playwright

### 2. Markdown Library
- **markdownify** (Recommended): Simple, good output
- **html2text**: More control, more complex
- **Go service**: Keep existing service via HTTP

### 3. Screenshot Handling
- Playwright built-in screenshot
- Return as bytes or base64
- Optional feature (can be disabled)

### 4. LLM Integration
- Use OpenAI API directly
- Support multiple providers (OpenAI, Anthropic, etc.)
- Optional feature

### 5. Package Name
- `firecrawl-standalone`: Distinguish from existing SDK
- `firecrawl-core`: If this becomes the main package
- Custom: User's choice

## Starting Code Skeleton

```python
# firecrawl/__init__.py
from .scraper import FirecrawlScraper
from .crawler import WebCrawler

__all__ = ['FirecrawlScraper', 'WebCrawler']

# firecrawl/scraper.py
from typing import Optional, List
from playwright.async_api import async_playwright
import httpx

class FirecrawlScraper:
    def __init__(self, use_playwright: bool = True):
        self.use_playwright = use_playwright

    async def scrape(self, url: str, formats: List[str] = None):
        if self.use_playwright:
            return await self._scrape_with_playwright(url, formats)
        else:
            return await self._scrape_with_http(url, formats)

    async def _scrape_with_playwright(self, url, formats):
        # Implementation
        pass

    async def _scrape_with_http(self, url, formats):
        # Implementation
        pass
```

## Success Criteria

### Minimal Viable Product (MVP)
- [x] Scrape single URL to markdown
- [x] Handle JavaScript-rendered pages
- [x] Crawl multiple pages
- [x] Respect robots.txt
- [x] Basic URL filtering
- [x] CLI interface

### Complete Solution
- [ ] All MVP features
- [ ] LLM extraction
- [ ] Screenshot capture
- [ ] Search integration
- [ ] Batch processing
- [ ] Full documentation
- [ ] Test coverage >80%

## Next Steps

1. **Create new directory**: `firecrawl-standalone/` in repo root
2. **Set up Python project**: pyproject.toml, requirements.txt
3. **Implement base scraper**: Start with HTTP engine
4. **Add Playwright support**: Handle JS sites
5. **Build markdown parser**: HTML → Markdown conversion
6. **Implement crawler**: Multi-page scraping
7. **Add CLI**: Command-line interface
8. **Write tests**: Ensure quality
9. **Document**: README and examples
10. **Package**: pip installable

## Estimated Complexity

- **MVP**: 3-5 days of focused development
- **Full feature parity**: 2-3 weeks
- **Production-ready**: 1 month (with testing, docs, polish)

---

**Ready to start!** The foundation is clear. Time to write some Python code.
