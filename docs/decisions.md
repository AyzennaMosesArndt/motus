# Architecture Decision Records — Motus

---

## ADR-001 — Deterministic 4-Stage Pipeline

**DATE:** 2026-05-23

**DECISION:** Deterministic 4-stage pipeline over agentic loops

**CONTEXT:**
Sports science enrichment needs consistency and auditability. Papers must be summarized and tagged reliably at scale (hundreds per day) with predictable cost and output quality.

**OPTIONS CONSIDERED:**

A) Agentic self-directing loops — LLM decides its own next steps, re-queries sources, re-tags autonomously. Flexible but unpredictable cost, hallucination risk compounds across iterations, hard to debug.

B) Deterministic pipeline stages — Researcher → Normalizer → Writer → Tagger → Verifier. Each stage has a single responsibility, fixed inputs/outputs, and explicit quality gates.

**CHOSEN:** B — Deterministic pipeline

**RATIONALE:**
- KISS: each stage is independently testable and debuggable
- Lower cost: one LLM call per paper per stage, predictable token usage
- No hallucination loops: writer and tagger are single-pass with 1 retry max
- Auditability: enrichment_status field tracks every paper through the pipeline
- Predictable output: confidence thresholds control what reaches the feed

**CONSEQUENCES:**
- Manual review queue (enrichment_status='needs_review') for low-confidence enrichments
- New source types require explicit routing logic in researcher.py
- Pipeline is not self-healing — failures are logged and require a re-run

---

## ADR-002 — Per-Field Confidence Scores in Enrichments

**DATE:** 2026-05-23

**DECISION:** Float 0.0–1.0 confidence score per extracted field (sports, body_regions, topics, evidence_level)

**CONTEXT:**
Tagger output quality varies by paper. Some papers clearly state the sport and evidence type; others require inference. We need a way to route low-quality enrichments to review without blocking high-confidence papers from the feed.

**OPTIONS CONSIDERED:**

A) Binary pass/fail per enrichment — simpler, but throws away useful partial signal. A paper with perfect sport/topic tags but uncertain evidence level gets rejected entirely.

B) Per-field float confidence — granular scoring allows partial auto-commit and targeted review of specific fields.

**CHOSEN:** B — Per-field confidence (0.0–1.0 float)

**RATIONALE:**
- Enables auto-commit for high-confidence papers (all scores ≥ 0.85)
- Enables targeted review: 0.60–0.84 goes to needs_review queue
- Enables rejection only for genuinely uncertain papers (any score < 0.60)
- CHECK constraints in Postgres enforce valid range at DB level

**CONSEQUENCES:**
- 4 additional float columns in enrichments table
- Tagger prompt must explicitly return confidence object in JSON schema
- Review UI (Phase 2) must expose per-field confidence to human reviewer
