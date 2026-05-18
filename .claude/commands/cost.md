# /cost
Report token usage and API cost for current session and last pipeline run.

## Steps
1. Read logs/pipeline_costs.jsonl (append-only cost log)
2. Summarize:
   - Session: tokens in / tokens out / estimated cost (USD)
   - Last /enrich run: papers processed / Haiku calls / Sonnet calls / total cost
   - Monthly rolling total (last 30 days from log)
3. Flag if monthly cost exceeds $10 threshold
