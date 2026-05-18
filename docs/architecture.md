# Architecture

## Overview
Personalized sports science discovery for endurance athletes.
Research index + LLM enrichment + 3D anatomy navigation.

## System diagram
```
PubMed API
Semantic Scholar API        →  Discovery Queue  →  Normalization
RSS Feeds                                              ↓
alphaXiv                                    Lightweight Research Index
                                                       ↓
                                            LLM Enrichment (Anthropic API)
                                              Writer → Tagger → Verifier
                                                       ↓
                                                  Postgres (Supabase)
                                                       ↓
                                            Next.js Frontend (Vercel)
                                                       ↓
                                            3D Anatomy Discovery UI
```

## Pipeline stages
See .claude/skills/ingestion-pipeline/SKILL.md

## Deploy targets
- Frontend: Vercel (Next.js, watches `deploy` branch)
- Worker: Railway (Python, watches `deploy` branch)
- DB: Supabase (managed Postgres)

## Key decisions
- No fulltext storage (legal + cost)
- No LangChain / vector DB / RAG
- Deterministic 4-stage pipeline, not agentic loops
- Haiku for enrichment at scale, Sonnet for quality checks
- GLTF anatomy model with React Three Fiber

## Data sources
See .claude/skills/research-knowledge/SKILL.md
