"""
URL filtering utilities for crawling.

This module provides utilities for filtering URLs during crawling.
"""

import logging
import re
from typing import Optional, List, Set
from urllib.parse import urlparse, urljoin
from fnmatch import fnmatch

logger = logging.getLogger(__name__)


class URLFilter:
    """
    Filter URLs based on various criteria.

    This class provides methods to filter URLs based on patterns,
    domains, depth, and other criteria.
    """

    def __init__(
        self,
        base_url: str,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        allow_backwards: bool = False,
        max_depth: int = 2
    ):
        """
        Initialize the URL filter.

        Args:
            base_url: The base URL of the website being crawled
            include_patterns: Regex patterns to include (None = all)
            exclude_patterns: Regex patterns to exclude
            allow_backwards: Allow crawling to parent directories
            max_depth: Maximum depth to follow links
        """
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.base_path = urlparse(base_url).path

        self.include_patterns = [re.compile(p) for p in (include_patterns or [])]
        self.exclude_patterns = [re.compile(p) for p in (exclude_patterns or [])]
        self.allow_backwards = allow_backwards
        self.max_depth = max_depth

        # Track URL depths
        self.url_depths: dict[str, int] = {base_url: 0}

    def should_crawl(self, url: str) -> bool:
        """
        Check if a URL should be crawled.

        Args:
            url: The URL to check

        Returns:
            True if the URL should be crawled, False otherwise
        """
        try:
            parsed = urlparse(url)

            # Must be http/https
            if parsed.scheme not in ("http", "https"):
                return False

            # Must be same domain
            if parsed.netloc != self.base_domain:
                return False

            # Check depth
            depth = self._get_depth(url)
            if depth > self.max_depth:
                return False

            # Check backwards crawling
            if not self.allow_backwards:
                if not url.startswith(self.base_path.rstrip("/") + "/"):
                    # Check if it's going backwards (to parent directory)
                    url_path = parsed.path
                    if not url_path.startswith(self.base_path):
                        return False

            # Check include patterns
            if self.include_patterns:
                if not any(p.search(url) for p in self.include_patterns):
                    return False

            # Check exclude patterns
            if self.exclude_patterns:
                if any(p.search(url) for p in self.exclude_patterns):
                    return False

            # Skip common non-content URLs
            if self._is_excluded_type(url):
                return False

            return True

        except Exception as e:
            logger.error(f"Error filtering URL {url}: {e}")
            return False

    def _get_depth(self, url: str) -> int:
        """
        Calculate the depth of a URL relative to base URL.

        Args:
            url: The URL to calculate depth for

        Returns:
            Depth level (0 = base URL)
        """
        if url in self.url_depths:
            return self.url_depths[url]

        parsed = urlparse(url)
        path = parsed.path.rstrip("/")

        # Calculate depth based on path segments
        base_segments = self.base_path.strip("/").split("/") if self.base_path != "/" else []
        url_segments = path.split("/")

        # Depth is how many segments beyond base
        depth = len(url_segments) - len(base_segments)

        self.url_depths[url] = depth
        return max(0, depth)

    def _is_excluded_type(self, url: str) -> bool:
        """
        Check if URL is an excluded type (files, etc.).

        Args:
            url: The URL to check

        Returns:
            True if excluded, False otherwise
        """
        # Skip common file extensions
        excluded_extensions = {
            ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z",
            ".exe", ".dmg", ".iso", ".bin",
            ".mp3", ".mp4", ".avi", ".mov", ".wav",
            ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
            ".woff", ".woff2", ".ttf", ".eot",
        }

        lower_url = url.lower()
        for ext in excluded_extensions:
            if lower_url.endswith(ext):
                return True

        return False

    def normalize_url(self, url: str) -> str:
        """
        Normalize a URL for consistent comparison.

        Args:
            url: The URL to normalize

        Returns:
            Normalized URL
        """
        parsed = urlparse(url)

        # Remove fragment
        normalized = parsed._replace(fragment="").geturl()

        # Remove trailing slash for consistency
        if normalized.endswith("/"):
            normalized = normalized[:-1]

        return normalized
