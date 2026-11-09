from app.services.crawlers.base import BaseCrawler
from app.services.crawlers.hfut_ci import HFUTCICrawler
from app.services.crawlers.hfut_som import HFUTSOMCrawler
from app.services.crawlers.manager import CrawlerManager

__all__ = ["BaseCrawler", "HFUTCICrawler", "HFUTSOMCrawler", "CrawlerManager"]
