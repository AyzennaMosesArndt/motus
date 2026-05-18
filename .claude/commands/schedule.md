# /schedule
Configure GitHub Actions cron for automated ingestion pipeline.

## Target file
.github/workflows/ingest.yml

## Schedule options
- Daily (recommended): cron: '0 6 * * *'  (06:00 UTC)
- Weekly: cron: '0 6 * * 1'               (Monday 06:00 UTC)

## Workflow steps
1. Checkout repo
2. Setup Python + install deps
3. Run: python pipeline/researcher.py --days 1
4. Run: python pipeline/normalizer.py
5. Run: python pipeline/writer.py --batch 50
6. Run: python pipeline/tagger.py --batch 50
7. Run: python pipeline/verifier.py
8. Log cost: append to logs/pipeline_costs.jsonl
9. On failure: send notification (GitHub Actions email default)

## Create the workflow file at .github/workflows/ingest.yml
