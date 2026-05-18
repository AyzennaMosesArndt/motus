---
name: enrichment
description: >
  Use when writing or modifying LLM enrichment prompts, structured output
  schemas, Writer stage logic, or Tagger stage extraction. Also load when
  debugging hallucinated tags or incorrect evidence levels.
---

# Enrichment

## Writer stage — summary prompt
Prompt file: apps/worker/prompts/writer_system.txt
Input: title + abstract
Output: max 120-word evidence-based summary

Tone rules:
- Factual and neutral
- No "you should", no coaching language
- No hedging ("it seems", "perhaps")
- Format: 2–3 sentences on finding + 1 sentence practical context for endurance athletes

## Tagger stage — structured extraction
Prompt file: apps/worker/prompts/tagger_system.txt

JSON schema (response_format: json_schema):
```json
{
  "sports": ["running", "cycling", "rowing", "skiing", "hyrox", "inline_skating"],
  "body_regions": ["calves", "quads", "hamstrings", "glutes", "core", "lower_back",
                   "hip_flexors", "knees", "achilles", "shoulders", "neck",
                   "grip_forearms", "hip_abductors", "ankles", "it_band"],
  "topics": ["recovery", "biomechanics", "nutrition", "vo2max", "sleep",
             "hrv", "injury", "strength", "altitude", "heat"],
  "evidence_level": 1,
  "sample_size": 42,
  "study_type": "RCT",
  "population": "trained"
}
```

Enums:
- sports: running | cycling | rowing | skiing | hyrox | inline_skating
- study_type: RCT | cohort | review | case_study | mechanistic | meta_analysis
- population: recreational | trained | elite | mixed | unknown
- evidence_level: 1–4 (see ingestion-pipeline skill)

## Verifier checks
- DOI regex: `^10\.\d{4,}/\S+$`
- Summary ≤ 150 words
- At least 1 sport tag
- Evidence level assigned (not null)
- No hallucinated journal names (cross-check source field)
- paper_id exists in papers table (FK integrity)

## Cost optimization
Use claude-haiku-4-5-20251001 for Writer + Tagger at scale.
Use claude-sonnet-4-6 only for quality checks or ambiguous papers.
Batch API calls where possible (up to 20 papers per run).
