import logging
from typing import List, Dict, Any
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from app.services.crawlers.base import BaseCrawler
from app.utils.extractor import (
    extract_publish_date,
    extract_deadline,
    categorize_item,
    infer_campus,
    extract_location,
    generate_tags
)

logger = logging.getLogger(__name__)

class HFUTSOMCrawler(BaseCrawler):
    """
    Crawler for HFUT School of Management (Information Management & Systems).
    Source: http://som.hfut.edu.cn/
    """
    source_name = "管理学院"
    base_url = "http://som.hfut.edu.cn/"

    target_sections = [
        {"url": "http://som.hfut.edu.cn/xyxw/tzgg.htm", "default_cat": "competition"},
        {"url": "http://som.hfut.edu.cn/xyxw/xsbg1.htm", "default_cat": "academic"}
    ]

    def crawl(self) -> List[Dict[str, Any]]:
        results = []
        seen_urls = set()

        for section in self.target_sections:
            section_url = section["url"]
            logger.info(f"Crawling HFUT SOM section: {section_url}")
            html = self.fetch_html(section_url)
            if not html:
                continue

            soup = BeautifulSoup(html, "html.parser")
            link_tags = soup.find_all("a", href=lambda h: h and "info/" in h)

            for a in link_tags:
                href = a.get("href")
                full_url = urljoin(section_url, href)

                if full_url in seen_urls:
                    continue
                seen_urls.add(full_url)

                item_data = self._parse_detail(full_url, section["default_cat"])
                if item_data:
                    results.append(item_data)

        logger.info(f"HFUT SOM crawler finished. Collected {len(results)} items.")
        return results

    def _parse_detail(self, url: str, fallback_cat: str) -> Dict[str, Any]:
        html = self.fetch_html(url)
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")

        # 1. Title
        title = ""
        title_tag = soup.find(class_="zw-title")
        if title_tag:
            title = title_tag.text.strip()
        elif soup.title:
            title = soup.title.text.split("-")[0].strip()

        if not title or len(title) < 4:
            return None

        # 2. Content
        content_div = soup.find("div", class_="v_news_content") or soup.find("div", class_="zw-txt")
        raw_text = self.clean_text(content_div.get_text()) if content_div else ""

        # 3. Publish Date
        other_div = soup.find(class_="zw-other")
        date_text = other_div.get_text() if other_div else raw_text[:200]
        pub_date = extract_publish_date(date_text)

        # 4. Intelligence Metadata
        category = categorize_item(title, raw_text)
        if category == "notice" and fallback_cat:
            category = fallback_cat

        campus = infer_campus(title, raw_text)
        deadline = extract_deadline(raw_text, default_year=pub_date.year)
        location = extract_location(raw_text)
        tags = generate_tags(title, raw_text)

        # 5. Brief summary
        summary = raw_text[:220].strip()
        if len(raw_text) > 220:
            summary += "..."

        return {
            "title": title,
            "category": category,
            "source_site": self.source_name,
            "campus": campus,
            "url": url,
            "content_raw": raw_text,
            "summary": summary,
            "publish_date": pub_date,
            "deadline": deadline,
            "location": location,
            "tags": tags,
            "view_count": 0
        }
