"""
Robots.txt handling for respectful crawling.

This module provides functionality to fetch, parse, and respect robots.txt files.
"""

import logging
from typing import Optional, Set
from urllib.parse import urlparse
import httpx
from urllib.robotparser import RobotFileParser

logger = logging.getLogger(__name__)


class RobotsChecker:
    """
    Fetch and parse robots.txt files.

    This class handles fetching and parsing robots.txt files to check
    if crawling is allowed for specific URLs.
    """

    def __init__(self, base_url: str, robots_txt: Optional[str] = None):
        """
        Initialize the robots.txt checker.

        Args:
            base_url: The base URL of the website
            robots_txt: Optional robots.txt content (if already fetched)
        """
        self.base_url = base_url
        self.parser = RobotFileParser()
        self.robots_url = self._get_robots_url()

        if robots_txt:
            self.parser.parse(robots_txt.splitlines())
        else:
            # Will be fetched on first use
            self.parser.set_url(self.robots_url)

    def _get_robots_url(self) -> str:
        """Get the URL of the robots.txt file."""
        parsed = urlparse(self.base_url)
        return f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    async def fetch(self) -> bool:
        """
        Fetch the robots.txt file from the server.

        Returns:
            True if fetched successfully, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.robots_url)

                if response.status_code == 200:
                    self.parser.parse(response.text.splitlines())
                    logger.info(f"Successfully fetched robots.txt from {self.robots_url}")
                    return True
                else:
                    logger.warning(
                        f"Could not fetch robots.txt from {self.robots_url}: "
                        f"Status {response.status_code}"
                    )
                    # If no robots.txt, allow all crawling
                    return False

        except Exception as e:
            logger.error(f"Error fetching robots.txt: {e}")
            # If we can't fetch robots.txt, allow all crawling
            return False

    def is_allowed(self, url: str, user_agent: str = "*") -> bool:
        """
        Check if crawling a URL is allowed by robots.txt.

        Args:
            url: The URL to check
            user_agent: The user agent to check (default: "*")

        Returns:
            True if allowed, False otherwise
        """
        try:
            return self.parser.can_fetch(user_agent, url)
        except Exception as e:
            logger.error(f"Error checking robots.txt for {url}: {e}")
            # If we can't determine, allow crawling
            return True
