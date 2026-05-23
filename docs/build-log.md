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

**Next:** Stage 3 — Supabase Schema
