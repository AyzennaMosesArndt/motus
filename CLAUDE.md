# Sports Science Intelligence Platform

## What this is
Personalized sports science discovery for endurance athletes (hobby & elite).
Research index + LLM enrichment + 3D anatomy navigation.
NOT an AI coach. NOT a training app. A research intelligence layer.

## Stack
- Frontend: Next.js 15, Tailwind, shadcn/ui, React Three Fiber
- Backend: Supabase (Postgres, Auth, Storage, Cron)
- Worker: Python (ingestion pipeline)
- AI: Anthropic API (structured outputs, deterministic prompting)
- Deploy: Vercel (frontend) + Railway (Python worker)
- CI: GitHub Actions

## Architecture — 4-Stage Pipeline
1. Researcher — discovers papers via PubMed / Semantic Scholar / RSS
2. Writer — generates short evidence-based summaries (Anthropic API)
3. Tagger — extracts sports, muscle groups, topics, evidence level
4. Verifier — checks DOI, deduplication, valid sources, sane tags

## Critical constraints
- Store ONLY: DOI, title, abstract, authors, journal, source_url, published_at + enrichment
- NEVER store: full PDFs, publisher HTML, paywalled content
- No LangChain, no vector DB, no RAG, no autonomous agents
- Deterministic pipeline stages — not agentic loops
- KISS: lightweight, deployable, maintainable

## Domain skills (load on demand)
- Ingestion work → ingestion-pipeline
- LLM prompts / tagging → enrichment
- 3D anatomy / body regions → anatomy-mapping
- DB schema / migrations → data-model
- React components / feed UI → frontend-patterns
- API queries / search terms → research-knowledge

## Parallel development workflow
- Feature work → always in a worktree: `claude --worktree feature/<name>`
- 2–4 subagents max (sweet spot)
- Agents: code-generator (build), code-reviewer (review), refactor-worker (cleanup)
- data-acquisition agent for API testing during development
- Deploy branch: merge only reviewed, tested code

## Branch → Deploy flow
`feature/*` → (review) → `main` → (tested) → `deploy`
Railway watches `deploy` branch. Vercel watches `deploy` branch.

## Context hygiene
- /compact before switching to a new major task
- /cost after long sessions
- /clear when context is polluted or task fully done
- Never @-include full files in CLAUDE.md — reference paths instead

## Commit style
Conventional Commits: feat:, fix:, chore:, docs:, pipeline:, data:

## Testing
- Python worker: pytest (apps/worker/tests/)
- Frontend: vitest + playwright for critical paths
