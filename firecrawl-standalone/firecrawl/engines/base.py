"""
Base engine interface for scraping engines.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from ..types import ScrapeOptions, ScrapeResult


class BaseEngine(ABC):
    """
    Abstract base class for scraping engines.

    All engines must implement the scrape method which takes a URL and options,
    and returns a ScrapeResult.
    """

    def __init__(self, options: Optional[ScrapeOptions] = None):
        """
        Initialize the engine with optional default options.

        Args:
            options: Default options to use for all scrapes
        """
        self.default_options = options or ScrapeOptions()

    @abstractmethod
    async def scrape(
        self,
        url: str,
        options: Optional[ScrapeOptions] = None
    ) -> ScrapeResult:
        """
        Scrape a URL and return the result.

        Args:
            url: The URL to scrape
            options: Options for this specific scrape (overrides defaults)

        Returns:
            ScrapeResult containing the scraped content
        """
        pass

    def _merge_options(self, options: Optional[ScrapeOptions]) -> ScrapeOptions:
        """Merge provided options with defaults."""
        if options is None:
            return self.default_options
        if self.default_options is None:
            return options
        # Create a merged options object
        merged = self.default_options.model_copy()
        for field, value in options.model_dump(exclude_unset=True).items():
            setattr(merged, field, value)
        return merged
