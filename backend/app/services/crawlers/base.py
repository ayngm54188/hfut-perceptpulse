import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from urllib.parse import urljoin
import httpx
from bs4 import BeautifulSoup

from app.utils.extractor import (
    extract_publish_date,
    extract_deadline,
    categorize_item,
    infer_campus,
    extract_location,
    generate_tags
)

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
}

class BaseCrawler(ABC):
    """
    Abstract base crawler for HFUT campus portals.
    """
    source_name: str = "合工大未知网站"
    base_url: str = ""

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout
        self.client = httpx.Client(
            headers=DEFAULT_HEADERS,
            timeout=timeout,
            follow_redirects=True,
            verify=False  # Skip SSL certificate issues on legacy campus portals
        )

    def fetch_html(self, url: str) -> str:
        """Fetches page content with encoding resolution."""
        try:
            resp = self.client.get(url)
            resp.raise_for_status()
            # Ensure proper Chinese UTF-8/GBK encoding
            content = resp.content
            # Detect BOM or meta charset
            for enc in ["utf-8", "gb18030", "gbk", resp.encoding]:
                if not enc:
                    continue
                try:
                    return content.decode(enc)
                except (UnicodeDecodeError, LookupError):
                    continue
            return resp.text
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return ""

    def clean_text(self, text: str) -> str:
        """Cleans excess whitespace, newlines, and tabs."""
        if not text:
            return ""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)

    @abstractmethod
    def crawl(self) -> List[Dict[str, Any]]:
        """
        Executes crawling logic and returns list of standardized intelligence item dicts.
        """
        pass
