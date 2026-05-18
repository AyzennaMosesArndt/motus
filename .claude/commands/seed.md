# /seed

Load an initial batch of papers for development and testing.

## Steps
1. `cd apps/worker`
2. `python pipeline/researcher.py --source pubmed --days 365 --limit 100`
3. `python pipeline/normalizer.py`
4. `python pipeline/writer.py --batch 50`
5. `python pipeline/tagger.py --batch 50`
6. `python pipeline/verifier.py`

## Purpose
Populate the local/staging DB with enough papers to:
- Test the feed UI
- Validate anatomy filtering
- Check sport + body_region tag distribution
- Test personalization logic

## Report
- Total papers seeded
- Sport distribution
- Evidence level distribution
- Any pipeline failures
