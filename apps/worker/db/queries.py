import os
from typing import Optional

from dotenv import load_dotenv
from supabase import create_client, Client

from utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

_client: Optional[Client] = None


def get_client() -> Client:
    global _client
    if _client is None:
        url = os.environ['SUPABASE_URL']
        key = os.environ['SUPABASE_SERVICE_ROLE_KEY']
        _client = create_client(url, key)
    return _client


def get_pending_queue(limit: int = 50) -> list[dict]:
    client = get_client()
    result = client.table('ingestion_queue').select('*').eq('status', 'pending').limit(limit).execute()
    return result.data or []


def update_queue_status(id: str, status: str, error: Optional[str] = None) -> None:
    client = get_client()
    payload: dict = {'status': status}
    if error:
        payload['error'] = error
    client.table('ingestion_queue').update(payload).eq('id', id).execute()


def insert_to_queue(raw: dict, source: str) -> None:
    client = get_client()
    client.table('ingestion_queue').insert({'raw': raw, 'source': source, 'status': 'pending'}).execute()


def insert_paper(paper: dict) -> str:
    client = get_client()
    result = client.table('papers').insert(paper).execute()
    return result.data[0]['id']


def paper_exists_by_doi(doi: str) -> bool:
    client = get_client()
    result = client.table('papers').select('id').eq('doi', doi).limit(1).execute()
    return bool(result.data)


def paper_exists_by_title_hash(title_hash: str) -> bool:
    # We store title hash check in-memory across the run; DB has no title_hash column
    # This function is a no-op hook for future DB-side dedup
    return False


def get_papers_without_enrichment(limit: int = 20) -> list[dict]:
    client = get_client()
    # LEFT JOIN equivalent: papers where no enrichment exists
    result = (
        client.table('papers')
        .select('*, enrichments(id)')
        .is_('enrichments.id', None)  # type: ignore[arg-type]
        .limit(limit)
        .execute()
    )
    return result.data or []


def insert_enrichment(enrichment: dict) -> str:
    client = get_client()
    result = client.table('enrichments').insert(enrichment).execute()
    return result.data[0]['id']


def update_enrichment(id: str, fields: dict) -> None:
    client = get_client()
    client.table('enrichments').update(fields).eq('id', id).execute()


def get_enrichments_pending_tags(limit: int = 20) -> list[dict]:
    client = get_client()
    result = (
        client.table('enrichments')
        .select('*, papers(*)')
        .is_('sports', None)
        .not_.in_('enrichment_status', ['failed'])
        .limit(limit)
        .execute()
    )
    return result.data or []


def get_enrichments_for_verification(limit: int = 50) -> list[dict]:
    client = get_client()
    result = (
        client.table('enrichments')
        .select('*, papers(*)')
        .in_('enrichment_status', ['auto_committed', 'needs_review'])
        .limit(limit)
        .execute()
    )
    return result.data or []
