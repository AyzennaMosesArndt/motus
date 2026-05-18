# /ingest

Run the discovery pipeline for new papers.

## Steps
1. `cd apps/worker`
2. `python pipeline/researcher.py --source pubmed --days 7`
3. `python pipeline/researcher.py --source semantic_scholar --days 7`
4. `python pipeline/normalizer.py`

## Report
- How many new papers queued
- How many duplicates skipped (DOI match)
- How many rejected (abstract too short / no DOI)
- Any API errors or rate limit hits
