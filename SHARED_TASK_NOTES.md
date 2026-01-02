# Firecrawl Python Refactoring - Shared Task Notes

## Project Goal
Refactor the entire Firecrawl project to encapsulate core functionality into Python scripts for easy integration into existing projects. Remove non-core code and documentation.

## Current State Analysis

### Project Structure
- **apps/api/**: Node.js/TypeScript API server (~111K lines of TypeScript code)
  - Core scraping logic in `src/scraper/`
  - API routes in `src/routes/`
  - Services and controllers
- **apps/python-sdk/**: Existing Python SDK (client library, not standalone)
- **apps/js-sdk/**: Node.js SDK
- **apps/rust-sdk/**: Rust SDK
- **apps/go-html-to-md-service/**: Go service for HTML to Markdown conversion
- **apps/playwright-service-ts/**: Playwright browser automation service

### Core Functionality to Extract
Based on the API and README, these are the core features:
1. **Scrape**: Single URL scraping (markdown, HTML, screenshots, structured data)
2. **Crawl**: Multi-page crawling with depth control
3. **Map**: URL discovery/mapping
4. **Search**: Web search integration
5. **Extract**: LLM-based structured data extraction

### Key Technical Components
- **WebScraper**: Main scraping engine (`src/scraper/WebScraper/`)
- **Playwright**: For JavaScript-rendered pages
- **Fire-engine**: Custom scraping engine
- **Go Markdown Service**: HTML-to-Markdown conversion
- **LLM Integration**: For structured data extraction
- **Queue System**: BullMQ for job processing
- **Authentication/Rate Limiting**: API key management

## Refactoring Approach

### Phase 1: Core Extraction (Recommended Next Step)
Extract the minimal viable scraping functionality into Python:
1. Identify core scraping logic (already in TypeScript/Node.js)
2. Port the WebScraper core to Python
3. Implement basic scrape/crawl functionality
4. Use existing Python libraries where possible (playwright, beautifulsoup, etc.)

### Phase 2: Service Integration
Integrate with external services:
1. Connect to Go Markdown Service (can run as separate process)
2. Integrate with existing Playwright service
3. Optional: Port these services to Python

### Phase 3: Advanced Features
Add remaining features:
1. LLM extraction
2. Search integration
3. Batch processing
4. Change tracking

### Phase 4: Cleanup
Remove non-core code and documentation

## Key Decisions Needed

1. **Service Dependencies**:
   - Keep Go Markdown Service as external dependency?
   - Keep Playwright service or use Python's playwright library?
   - How to handle queue system (BullMQ is Node.js specific)?

2. **Architecture**:
   - Standalone Python scripts vs Python package?
   - CLI tool vs library vs both?
   - How to handle configuration?

3. **Feature Parity**:
   - Which features are essential for v1?
   - Which can be skipped or simplified?

## Next Steps for Next Iteration

1. **Explore Core Scraping Logic**:
   - Read `apps/api/src/scraper/WebScraper/` to understand core algorithm
   - Identify external dependencies
   - Map out the scraping flow

2. **Identify Python Equivalents**:
   - Playwright Python: `playwright` package
   - HTML parsing: `beautifulsoup4`, `lxml`
   - Markdown conversion: `markdownify`, or keep Go service
   - HTTP client: `httpx`, `aiohttp`
   - Queue system: `celery`, `arq`, or custom

3. **Create Proof of Concept**:
   - Build minimal scraper in Python
   - Test with a few URLs
   - Compare output with original

## Files to Investigate

- `apps/api/src/scraper/WebScraper/` - Core scraping logic
- `apps/api/src/scraper/scrapeURL/` - URL scraping implementation
- `apps/api/src/routes/v2/` - V2 API endpoints (latest API design)
- `apps/api/src/config.ts` - Configuration options
- `apps/api/src/lib/` - Utility libraries

## Important Notes

- The existing `apps/python-sdk/` is a **client SDK** for the API, not a standalone scraper
- Core scraping logic is in TypeScript/Node.js - needs porting to Python
- Multiple services (Go, Playwright) can be run as external processes
- The project uses BullMQ (Node.js) for job queues - needs Python equivalent
- Consider using existing Python scraping libraries (scrapy, selenium) as foundation
