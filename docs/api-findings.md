# API Findings — Motus Data Sources

Living document. Last updated: 2026-05-23 (Stage 2 API exploration).

---

## SOURCE: PubMed

ENDPOINT: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/

RESPONSE_SHAPE:
- esearch returns: esearchresult.count, esearchresult.idlist[]
- efetch (XML) returns: ArticleTitle, Abstract/AbstractText, AuthorList/Author[], Journal/Title, ArticleId[@IdType=doi], ArticleId[@IdType=pubmed]

FIELDS_AVAILABLE: doi, title, abstract, authors, journal, source_id (PMID), published_at, source_url, source_name

FIELDS_MISSING: none — all papers table fields mappable

SOURCE_NAME: 'pubmed'
SOURCE_URL construction: f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
SOURCE_ID: PMID string

RATE_LIMIT: 0.1s/req with API key (confirmed — key present and non-empty)

PAGINATION: usehistory=y + WebEnv + query_key + retstart/retmax (batch up to 200 PMIDs per efetch)

SAMPLE_COUNT (with DATE_FILTER 2018–present):
- "endurance running"[TIAB]: 381 papers
- "marathon running"[TIAB]: 270 papers
- "running economy"[TIAB]: 519 papers

API_KEY_APPENDED: confirmed — appended to every esearch and efetch request

FIELD_MAPPING_CONFIRMED:
- Title: present (full text)
- Abstract: present, 282 words on test paper (above 80-word threshold)
- Authors: 4 on test paper
- Journal: "Journal of strength and conditioning research"
- DOI: present via ArticleId[@IdType=doi]
- PMID: present via ArticleId[@IdType=pubmed]

IMPORTANT: efetch retmode=json has inconsistent nested structure — use retmode=xml instead. XML parsing via ElementTree is reliable.

RECOMMENDATION: primary source — best metadata, highest signal, 65 queries expected to yield 300–800 unique papers per run

---

## SOURCE: arXiv

ENDPOINT: https://export.arxiv.org/api/query (HTTPS required — HTTP 301 redirects, use curl -L or requests allow_redirects=True)

RESPONSE_SHAPE: Atom XML feed. Namespaces: http://www.w3.org/2005/Atom (entries), http://a9.com/-/spec/opensearch/1.1/ (totalResults)

FIELDS_AVAILABLE: title, summary (abstract), author[], published, id (arxiv URL)

FIELDS_MISSING: doi (absent — not assigned for most preprints), journal (use 'arXiv' as constant)

SOURCE_NAME: 'arxiv'
SOURCE_URL: entry.id value (e.g. "http://arxiv.org/abs/2412.15076v4") — used as BOTH source_id AND source_url
SOURCE_ID: same as source_url (arxiv abs URL)
DOI: None for most — leave null, do not fabricate

RATE_LIMIT: 0.5s between requests

PAGINATION: start parameter + max_results

SAMPLE_COUNT:
- "endurance running physiology": 68,596 total (very broad — arXiv is not sports-science-specific)
- "VO2max endurance training": 259,007 total

IMPLEMENTATION NOTES:
- Must use HTTPS (follow 301 redirect from HTTP)
- DOI not present in link elements — use entry `id` (arxiv URL) as source_id
- Signal ratio is low: arXiv has minimal sports physiology content — supplementary only
- Abstract is `{atom}summary` element

RECOMMENDATION: supplementary — flag source_name='arxiv', lower priority in feed

---

## SOURCE: Crossref

ENDPOINT: https://api.crossref.org/works/{doi}

RESPONSE_SHAPE: JSON with message.DOI, message.title[], message.author[], message.container-title[], message.published.date-parts, message.abstract (often absent)

FIELDS_AVAILABLE: doi, title, authors, journal, published_at

FIELDS_MISSING: abstract almost always absent (paywalled journal content not included by Crossref)

SOURCE_NAME: 'rss' (when discovered via RSS → Crossref enrichment) or keep original source_name
SOURCE_URL: feed_entry.link (the RSS item link, stored as source_url)
SOURCE_ID: message.DOI (use DOI as source_id for Crossref-enriched rows)
NOTE: Crossref is enrichment only — it does not create new rows, it adds metadata to RSS-discovered rows. Never set source_name='crossref'.

RATE_LIMIT: 0.5s between requests (polite pool via User-Agent header)

PAGINATION: N/A — single DOI lookups only (not used for discovery)

FIELD_MAPPING_CONFIRMED (DOI: 10.1136/bjsports-2020-103769):
- DOI: 10.1136/bjsports-2020-103769 ✓
- title: present ✓
- abstract: absent (expected — BJSM is paywalled)
- authors count: 4 ✓
- journal: "British Journal of Sports Medicine" ✓
- published date-parts: [2021, 4, 9] ✓
- User-Agent polite pool header: confirmed working

USE CASE: validation and enrichment only — NOT for discovery. Use to confirm DOI exists and get published_at when RSS provides only a link.

RECOMMENDATION: validation/enrichment — call after RSS discovery, not as primary source

---

## SOURCE: RSS (BJSM — British Journal of Sports Medicine)

ENDPOINT: https://bjsm.bmj.com/rss/current.xml

RESPONSE_SHAPE: RSS 1.0 / RDF format (NOT standard RSS 2.0). Namespace: http://purl.org/rss/1.0/

FIELDS_AVAILABLE per item:
- rss:title — article title ✓
- rss:link — URL (bjsm.bmj.com/cgi/content/short/...) ✓
- PRISM doi field: absent in this feed

FIELDS_MISSING: doi (not in link or PRISM namespace), abstract, authors, pubDate

SAMPLE_COUNT: 14 items (current issue May 2026)

IMPLEMENTATION NOTES:
- RSS 1.0 / RDF format — feedparser handles this transparently (recommended)
- DOI is NOT extractable from link URL (/cgi/content/short/60/10/683?rss=1)
- Correct flow: RSS entry → extract title → PubMed title search → get full metadata
- When doi=None from link, try Crossref as fallback

RECOMMENDATION: discovery trigger — RSS tells us new papers exist; always fetch full metadata via PubMed title search. Do not use RSS metadata directly.

---

## SOURCE: Semantic Scholar (LEER-ROHR)

ENDPOINT: https://api.semanticscholar.org/graph/v1/ (not tested)

NOTE: Leer-rohr pattern — skipped entirely when SEMANTIC_SCHOLAR_API_KEY is absent or empty.

Expected behavior when key not configured:
```
WARNING: Semantic Scholar key not configured — skipping source
```

Leer-rohr implementation:
```python
key = os.getenv('SEMANTIC_SCHOLAR_API_KEY', '')
if not key or not key.strip():
    self.logger.warning("Semantic Scholar key not configured — skipping source")
    return []
```

FIELDS_AVAILABLE (when key present):
- doi (via externalIds.DOI), title, abstract, authors[].name, publicationVenue.name (journal), publicationDate, paperId

FIELDS_MISSING: none when key present — all papers table fields mappable

SOURCE_NAME: 'semantic_scholar'
SOURCE_URL: f"https://www.semanticscholar.org/paper/{paperId}"
SOURCE_ID: paperId string

RECOMMENDATION: secondary — enable when key confirmed valid; graceful skip otherwise

---

## Summary

| Source | source_name | Signal | DOI | Abstract | Rate Limit | Recommendation |
|--------|-------------|--------|-----|----------|------------|----------------|
| PubMed | 'pubmed' | High | Yes (most) | Yes | 0.1s/req (with key) | Primary — 65 queries |
| arXiv | 'arxiv' | Low | No | Yes | 0.5s/req | Supplementary |
| Crossref | (enrichment only) | N/A | Yes | No | 0.5s/req | Validation — not discovery |
| RSS | 'rss' | High trigger | No (in feed) | No | 1x/day | Discovery trigger → PubMed lookup |
| Semantic Scholar | 'semantic_scholar' | Medium | Yes | Yes | 1.1s/req | Secondary (leer-rohr) |
