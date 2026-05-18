# /enrich

Run LLM enrichment on queued papers (Writer + Tagger + Verifier stages).

## Steps
1. `cd apps/worker`
2. `python pipeline/writer.py --batch 20`
3. `python pipeline/tagger.py --batch 20`
4. `python pipeline/verifier.py`

## Report
- Enriched count
- Failed count + reasons
- Evidence level distribution (1–4)
- Sports tag distribution
- Any papers rejected by verifier (missing DOI, bad tags, duplicate)
