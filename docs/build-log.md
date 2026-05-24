# Motus — Build Log

---

## [Stage 0 — Rename + GitHub + Init] ✅

**Completed:**
- Project renamed from "sports-science-platform" to "motus" across README.md, CLAUDE.md
- GitHub repo created: https://github.com/AyzennaMosesArndt/motus (public)
- Both `main` and `deploy` branches pushed to origin
- Supabase CLI installed (2.101.0)
- Doctor checks: all tools present, .env.local verified
- docs/decisions.md created (ADR-001 pipeline, ADR-002 confidence scoring)
- docs/build-log.md initialized

**Commit:** a99fff7

**Next:** Stage 1 — Environment Setup (complete — see below)

---

## [Stage 1 — Environment Setup] ✅

**Completed:**
- .env.example created (all 10 keys documented)
- Python venv: apps/worker/.venv/ (Python 3.11.9)
- requirements.txt: httpx, supabase, anthropic, feedparser, pytest + pins
- runtime.txt: python-3.11.9
- Full directory structure created (24 placeholder files):
  pipeline/ sources/ db/ prompts/ utils/ logs/ tests/
- All packages installed via pip

**Commit:** (pending)

**Next:** Stage 2 — Data Pipeline Specification + API Exploration (complete — see below)

---

## [Stage 2 — Data Pipeline Spec + API Exploration] ✅

**Completed:**
- docs/data-pipeline-spec.md written (65 PubMed queries, 10 arXiv, 10 S2, 6 RSS feeds, full taxonomy, field mappings, quality filters, rate limits)
- Live API tests against PubMed, arXiv, Crossref, RSS (BJSM)
- PubMed: 381/270/519 papers for 3 test queries, field mapping confirmed, API key confirmed
- arXiv: HTTPS redirect noted, source_url=entry.id, signal ratio low
- Crossref: abstract absent (paywalled), polite User-Agent confirmed, validation-only use
- RSS/BJSM: RSS 1.0 RDF format, 14 items, DOI not in URL — feedparser + PubMed lookup pattern
- Semantic Scholar: leer-rohr pattern documented, field mappings for when key available
- docs/api-findings.md updated with all source_name values, source_url construction, complete field mappings
- Code review: NEEDS_CHANGES → fixed critical field mapping gaps → PASS

**Commit:** (pending)

**Next:** Stage 3 — Supabase Schema (complete — see below)

---

## [Stage 3 — Database Schema] ✅

**Completed:**
- 6 SQL migrations: papers, enrichments, users, saves, ingestion_queue, RLS
- Code review: NEEDS_CHANGES → fixed 3 criticals:
  - paper_id NOT NULL on enrichments
  - enrichment_status CHECK constraint (7 valid values)
  - WITH CHECK (true) on service_role ingestion_queue policy
- Added: anon read policies for public browsing, saves(paper_id) index, GRANT statements
- TypeScript types: apps/web/types/supabase.ts (handwritten from schema)
- Supabase project reachable (200 OK), tables exist
- CLI link pending: run `supabase login --token <PAT>` then `supabase db push`

**Commit:** (pending)

**Next:** Stage 4 — Python Ingestion Pipeline

---

## [Stage 4 — Python Ingestion Pipeline] ✅

**Completed:**
- researcher.py: PubMed / Semantic Scholar / arXiv / RSS discovery, shared cross-source dedup sets, report logging
- normalizer.py: abstract length gate (80 words), identifier check, cutoff date 2018, DOI dedup, field projection
- writer.py: Anthropic API (haiku), 120-word limit, coaching/hedge phrase detection, 1 retry, cost logging
- tagger.py: JSON extraction with allowlists, per-field confidence thresholds (0.60 / 0.85), status assignment
- verifier.py: soft-reject policy gates (no sport, no evidence level, long summary, invalid DOI, all confidence < 0.60)
- conftest.py: sys.path setup for pytest
- test_normalizer.py: 26 tests covering word_count, _parse_date, _validate (8 cases), _normalize_paper, title_hash
- test_verifier.py: 19 tests covering DOI regex, _verify_enrichment (all gate combinations)
- 45/45 tests passing

**Commit:** (pending)

**Next:** Stage 5 — Frontend feed UI
