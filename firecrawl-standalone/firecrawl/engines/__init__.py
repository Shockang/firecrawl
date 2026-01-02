"""
Scraping engines for different use cases.
"""

from .base import BaseEngine
from .http import HTTPEngine
from .playwright import PlaywrightEngine

__all__ = ["BaseEngine", "HTTPEngine", "PlaywrightEngine"]
