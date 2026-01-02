"""
Type definitions for Firecrawl Standalone.
"""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class EngineType(str, Enum):
    """Available scraping engines."""
    HTTP = "http"
    PLAYWRIGHT = "playwright"


class OutputFormat(str, Enum):
    """Output format options."""
    MARKDOWN = "markdown"
    HTML = "html"
    SCREENSHOT = "screenshot"


class ScrapeOptions(BaseModel):
    """Options for scraping a single URL."""
    formats: List[OutputFormat] = Field(
        default_factory=lambda: [OutputFormat.MARKDOWN],
        description="Output formats to generate"
    )
    screenshot: bool = Field(
        default=False,
        description="Capture screenshot of the page"
    )
    headers: Optional[Dict[str, str]] = Field(
        default=None,
        description="Custom HTTP headers"
    )
    timeout: int = Field(
        default=30000,
        description="Timeout in milliseconds"
    )
    only_main_content: bool = Field(
        default=True,
        description="Extract only the main content, skip navigation/footers"
    )
    wait_for: Optional[int] = Field(
        default=None,
        description="Wait time in milliseconds after page load"
    )
    engine: EngineType = Field(
        default=EngineType.HTTP,
        description="Which engine to use for scraping"
    )

    @field_validator("formats")
    @classmethod
    def validate_formats(cls, v):
        if not v:
            return [OutputFormat.MARKDOWN]
        return v


class CrawlOptions(BaseModel):
    """Options for crawling a website."""
    max_pages: int = Field(
        default=10,
        description="Maximum number of pages to crawl"
    )
    max_depth: int = Field(
        default=2,
        description="Maximum depth to follow links"
    )
    include_patterns: Optional[List[str]] = Field(
        default=None,
        description="URL patterns to include (regex)"
    )
    exclude_patterns: Optional[List[str]] = Field(
        default=None,
        description="URL patterns to exclude (regex)"
    )
    allow_backwards: bool = Field(
        default=False,
        description="Allow crawling to parent directories"
    )
    ignore_sitemap: bool = Field(
        default=False,
        description="Ignore sitemap.xml for initial URL discovery"
    )
    scrape_options: Optional[ScrapeOptions] = Field(
        default=None,
        description="Options to use when scraping each page"
    )


class ScrapeResult(BaseModel):
    """Result from scraping a single URL."""
    url: str = Field(description="The URL that was scraped")
    markdown: Optional[str] = Field(
        default=None,
        description="Content in markdown format"
    )
    raw_html: Optional[str] = Field(
        default=None,
        description="Raw HTML content"
    )
    screenshot: Optional[str] = Field(
        default=None,
        description="Base64 encoded screenshot"
    )
    status_code: int = Field(
        default=200,
        description="HTTP status code"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if scraping failed"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the scrape"
    )

    @property
    def success(self) -> bool:
        """Check if the scrape was successful."""
        return self.error is None and (self.markdown or self.raw_html)
