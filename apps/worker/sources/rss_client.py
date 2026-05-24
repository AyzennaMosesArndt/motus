import re
import time
from typing import Optional

import feedparser
from dotenv import load_dotenv

from sources.crossref_client import CrossrefClient
from utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

RSS_FEEDS = [
    'https://bjsm.bmj.com/rss/current.xml',
    'https://journals.physiology.org/action/showFeed?type=etoc&feed=rss&jc=jappl',
    'https://journals.humankinetics.com/rss/journals/ijsnem',
    'https://www.tandfonline.com/action/showFeed?type=etoc&feed=rss&jc=tejs20',
    'https://link.springer.com/search.rss?query=endurance+exercise&facet-journal-id=40279',
    'https://www.frontiersin.org/journals/physiology/rss',
]

DOI_PATTERN = re.compile(r'10\.\d{4,}/[^\s"<>]+')


class RSSClient:
    def __init__(self) -> None:
        self.crossref = CrossrefClient()

    def fetch_all(self) -> list[dict]:
        results: list[dict] = []
        for feed_url in RSS_FEEDS:
            try:
                entries = self._fetch_feed(feed_url)
                results.extend(entries)
                logger.info(f'RSS fetched {len(entries)} entries from {feed_url[:60]}')
            except Exception as e:
                logger.error(f'RSS feed error for {feed_url[:60]}: {e}')
        return results

    def _fetch_feed(self, url: str) -> list[dict]:
        feed = feedparser.parse(url)
        results = []
        for entry in feed.entries:
            link = getattr(entry, 'link', '') or ''
            doi = self._extract_doi(link)
            if doi:
                enriched = self.crossref.lookup_doi(doi)
                if enriched:
                    enriched['source_url'] = link
                    enriched['source_name'] = 'rss'
                    results.append(enriched)
                    continue
            # Fallback: minimal record from RSS entry alone
            title = getattr(entry, 'title', '')
            if title:
                results.append({
                    'title': title,
                    'abstract': None,
                    'authors': [],
                    'journal': None,
                    'doi': None,
                    'source_id': None,
                    'source_name': 'rss',
                    'source_url': link,
                    'published_at': getattr(entry, 'published', None),
                })
        return results

    def _extract_doi(self, url: str) -> Optional[str]:
        m = DOI_PATTERN.search(url)
        return m.group() if m else None
