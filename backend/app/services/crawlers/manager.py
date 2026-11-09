import logging
from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.item import PulseItem, CrawlSource
from app.services.crawlers.hfut_ci import HFUTCICrawler
from app.services.crawlers.hfut_som import HFUTSOMCrawler

logger = logging.getLogger(__name__)

class CrawlerManager:
    """
    Orchestrates campus crawlers, deduplicates items against SQLite,
    and updates intelligence records.
    """

    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()
        self._own_db = db is None
        self.crawlers = [
            HFUTCICrawler(),
            HFUTSOMCrawler()
        ]

    def run_all(self) -> Dict[str, Any]:
        """Runs all registered crawlers and stores unique items."""
        total_scraped = 0
        new_inserted = 0
        skipped_existing = 0
        sources_seen = set()

        now = datetime.now()

        try:
            for crawler in self.crawlers:
                logger.info(f"Starting crawler: {crawler.source_name}")
                sources_seen.add(crawler.source_name)

                try:
                    items = crawler.crawl()
                except Exception as e:
                    logger.error(f"Error executing crawler {crawler.source_name}: {e}")
                    continue

                total_scraped += len(items)

                for item_dict in items:
                    url = item_dict.get("url")
                    if not url:
                        continue

                    # Deduplication check in SQLite
                    existing = self.db.query(PulseItem).filter(PulseItem.url == url).first()
                    if existing:
                        skipped_existing += 1
                        # If existing item lacks summary or deadline, patch it
                        if not existing.deadline and item_dict.get("deadline"):
                            existing.deadline = item_dict["deadline"]
                        if not existing.location and item_dict.get("location"):
                            existing.location = item_dict["location"]
                        continue

                    # Insert new item
                    new_item = PulseItem(**item_dict)
                    self.db.add(new_item)
                    new_inserted += 1

                # Update CrawlSource last_crawled_at
                source_record = self.db.query(CrawlSource).filter(
                    CrawlSource.name.like(f"%{crawler.source_name}%")
                ).first()
                if source_record:
                    source_record.last_crawled_at = now

                self.db.commit()

        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed during crawler persistence: {e}")
            raise
        finally:
            if self._own_db:
                self.db.close()

        result = {
            "status": "success",
            "timestamp": now.isoformat(),
            "total_scraped": total_scraped,
            "new_inserted": new_inserted,
            "skipped_existing": skipped_existing,
            "sources": list(sources_seen)
        }
        logger.info(f"Crawl batch finished: {result}")
        return result
