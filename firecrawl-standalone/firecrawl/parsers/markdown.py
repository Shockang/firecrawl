"""
HTML to Markdown converter.

This module handles conversion of HTML content to clean markdown format.
"""

import logging
import re
from typing import Optional, Set
from bs4 import BeautifulSoup
from markdownify import markdownify as md

logger = logging.getLogger(__name__)


class HTMLToMarkdown:
    """
    Convert HTML content to markdown format.

    This class provides methods to convert HTML to clean, readable markdown
    by removing unwanted elements and formatting the content properly.
    """

    # Tags to remove completely
    REMOVE_TAGS = {
        "script", "style", "iframe", "noscript", "meta", "link",
        "head", "svg", "path", "g", "defs", "use", "symbol"
    }

    # Tags that typically contain non-main content
    NON_MAIN_CONTENT_SELECTORS = [
        "nav", "footer", "header", "aside",
        "[role='navigation']", "[role='complementary']",
        "[role='banner']", "[role='contentinfo']",
        ".sidebar", ".navigation", ".footer", ".header",
        "#sidebar", "#navigation", "#footer", "#header",
        ".menu", ".breadcrumb", ".pagination",
        ".cookie-banner", ".popup", ".modal",
        "iframe", "ins", "ads", ".advertisement"
    ]

    def __init__(self):
        """Initialize the converter."""
        self.logger = logger

    async def convert(
        self,
        html: str,
        base_url: Optional[str] = None,
        only_main_content: bool = True
    ) -> str:
        """
        Convert HTML to markdown.

        Args:
            html: Raw HTML content
            base_url: Base URL for resolving relative links
            only_main_content: If True, remove nav/footers/etc

        Returns:
            Converted markdown content
        """
        try:
            # Parse HTML
            soup = BeautifulSoup(html, "lxml")

            if only_main_content:
                soup = self._extract_main_content(soup)
            else:
                # Just remove unwanted tags
                for tag in self.REMOVE_TAGS:
                    for element in soup.find_all(tag):
                        element.decompose()

            # Convert to markdown
            markdown = md(str(soup), heading_style="ATX")

            # Clean up the markdown
            markdown = self._clean_markdown(markdown)

            return markdown.strip()

        except Exception as e:
            self.logger.error(f"Error converting HTML to markdown: {e}")
            return ""

    def _extract_main_content(self, soup: BeautifulSoup) -> BeautifulSoup:
        """
        Extract only the main content from HTML.

        This removes navigation, footers, headers, and other non-content elements.
        """
        # Remove non-main content elements
        for selector in self.NON_MAIN_CONTENT_SELECTORS:
            try:
                for element in soup.select(selector):
                    element.decompose()
            except Exception as e:
                self.logger.debug(f"Error removing selector {selector}: {e}")

        # Remove unwanted tags
        for tag in self.REMOVE_TAGS:
            for element in soup.find_all(tag):
                element.decompose()

        # Try to find main content area
        main_content = (
            soup.find("main") or
            soup.find("article") or
            soup.find(id="main") or
            soup.find(id="content") or
            soup.find(class_="content") or
            soup.find(role="main") or
            soup.body
        )

        if main_content:
            # Create new soup with just the main content
            new_soup = BeautifulSoup("<html><body></body></html>", "lxml")
            new_soup.body.append(main_content.extract())
            return new_soup

        return soup

    def _clean_markdown(self, markdown: str) -> str:
        """
        Clean up the markdown output.

        This removes excessive whitespace, empty lines, etc.
        """
        # Remove excessive blank lines (more than 2)
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)

        # Remove leading/trailing whitespace from each line
        lines = [line.strip() for line in markdown.split('\n')]
        markdown = '\n'.join(lines)

        # Remove multiple spaces (but preserve in code blocks)
        in_code_block = False
        cleaned_lines = []
        for line in lines:
            if line.startswith('```'):
                in_code_block = not in_code_block
            if not in_code_block:
                # Remove multiple spaces but preserve single
                line = re.sub(r' +', ' ', line)
            cleaned_lines.append(line)

        return '\n'.join(cleaned_lines)

    def extract_links(self, html: str, base_url: Optional[str] = None) -> Set[str]:
        """
        Extract all unique links from HTML.

        Args:
            html: Raw HTML content
            base_url: Base URL for resolving relative links

        Returns:
            Set of unique URLs found in the HTML
        """
        soup = BeautifulSoup(html, "lxml")
        links = set()

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"].strip()

            # Skip empty links, anchors, javascript, mailto
            if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
                continue

            # Resolve relative URLs if base_url provided
            if base_url and not href.startswith(("http://", "https://")):
                from urllib.parse import urljoin
                href = urljoin(base_url, href)

            # Only include http/https links
            if href.startswith(("http://", "https://")):
                links.add(href)

        return links
