---
name: research-knowledge
description: >
  Use when working on ingestion pipeline, API queries, search term
  optimization, or data source evaluation. Contains best APIs, query
  strategies, rate limits, field mappings, and curated search terms
  for sports science paper discovery. Also auto-loaded by data-acquisition agent.
---

# Research Knowledge — Sports Science Data Sources

## Primary APIs

### PubMed / NCBI E-utilities
Base URL: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
Key endpoints:
  esearch.fcgi  → search, returns IDs
  efetch.fcgi   → fetch full records (XML or JSON)
  einfo.fcgi    → DB metadata

Rate limit: 10 req/s with API key ($PUBMED_API_KEY), 3 req/s without
Pagination: usehistory=y + WebEnv + query_key + retstart/retmax
Recommended batch: retmax=100 per fetch

Best search terms (use [TIAB] = title+abstract field):
```
# Running / endurance
"endurance running"[TIAB] OR "distance running"[TIAB] OR "marathon"[TIAB]
"running economy"[TIAB] OR "running biomechanics"[TIAB]

# Cycling
"endurance cycling"[TIAB] OR "road cycling performance"[TIAB]
"cycling power output"[TIAB] OR "cyclist physiology"[TIAB]

# Rowing / Hyrox / multi-sport
"rowing performance"[TIAB] OR "ergometer"[TIAB]
"functional fitness"[TIAB] OR "obstacle racing"[TIAB]

# Physiology
"maximal oxygen uptake"[TIAB] OR "VO2max"[TIAB]
"lactate threshold"[TIAB] OR "anaerobic threshold"[TIAB]

# Recovery & load
"exercise recovery"[TIAB] OR "post-exercise"[TIAB]
"heart rate variability"[TIAB] AND "exercise"[TIAB]
"training load"[TIAB] AND ("running"[TIAB] OR "cycling"[TIAB])

# Nutrition
"endurance nutrition"[TIAB] OR "carbohydrate loading"[TIAB]
"sports nutrition"[TIAB] AND "endurance"[TIAB]

# Injury
"running injury"[TIAB] OR "achilles tendinopathy"[TIAB]
"patellofemoral"[TIAB] OR "iliotibial band"[TIAB]

# Date filter (always append)
AND ("2018/01/01"[PDAT] : "3000"[PDAT])
```

PubMed field mapping → papers table:
```
MedlineCitation/PMID          → source_id
ArticleTitle                  → title
AbstractText (join if list)   → abstract
AuthorList/Author             → authors[] (LastName + ForeName)
Journal/Title                 → journal
PubDate (Year+Month+Day)      → published_at
ArticleId[@IdType="doi"]      → doi
```

---

### Semantic Scholar
Base URL: https://api.semanticscholar.org/graph/v1/
Key endpoints:
  GET /paper/search        → keyword search
  POST /paper/batch        → fetch multiple by ID

Rate limit: 1 req/s without key → get free API key ($SEMANTIC_SCHOLAR_KEY)
Fields param (always specify to avoid fetching junk):
  title,abstract,authors,journal,publicationDate,externalIds,
  citationCount,isOpenAccess,openAccessPdf

Best for:
  - Citation count (signal for paper importance)
  - Open access detection (isOpenAccess flag)
  - Cross-referencing DOIs from PubMed

Semantic Scholar field mapping → papers table:
```
paperId                       → source_id
title                         → title
abstract                      → abstract
authors[].name                → authors[]
publicationVenue.name         → journal
publicationDate               → published_at (ISO format, parse carefully)
externalIds.DOI               → doi
```

---

### RSS Feeds (Discovery triggers only — not main data source)
Use as: new paper signal → then fetch full metadata via PubMed/S2

Recommended feeds:
  BJSM:        https://bjsm.bmj.com/rss/current.xml
  IJSPP:       https://journals.humankinetics.com/rss/journals/ijspp
  PubMed saved search RSS: construct via NCBI → Save Search → Create RSS

RSS gives: title, link, pubDate, description (truncated abstract)
Always fetch full abstract via PubMed efetch after RSS discovery.

---

### alphaXiv
Use for: open-access preprints (physiology, biomechanics, sports science adjacent)
Not a primary source — supplement only when PubMed/S2 miss coverage.
Search API: https://alphaXiv.org/api (check current docs — API evolving)

---

## Editorial / High Quality Sources (manual curation candidates)
- BJSM (British Journal of Sports Medicine) — tier 1
- Sweat Science (Alex Hutchinson) — tier 1 review writing
- TrainingPeaks blog — tier 2 practical
- Sigma Nutrition — tier 1 nutrition evidence

---

## Quality signals for paper selection
Strong signals (prioritize):
  - RCT or meta-analysis (evidence_level = 1)
  - Sample size > 20
  - Population: trained or elite athletes
  - Journal impact factor > 2.0

Weak signals (flag, don't auto-reject):
  - Case study or mechanistic (evidence_level = 3/4)
  - Sample size < 10
  - Population: sedentary or clinical

---

## Rate limit safety — recommended delays
PubMed without key:   0.4s between requests (stay under 3/s)
PubMed with key:      0.1s between requests
Semantic Scholar:     1.1s between requests (stay under 1/s)
RSS:                  no strict limit, poll max once per hour
