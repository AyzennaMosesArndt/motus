# /explore-source

Test a data source and document findings.

## Arguments
SOURCE: pubmed | semantic_scholar | rss | alphaxiv

## Steps
1. Load skill: research-knowledge (query patterns + field mappings)
2. Spawn data-acquisition agent with SOURCE as target:
   - Fire 3 test queries against SOURCE using best known search terms
   - Inspect response shape and available fields
   - Check rate limit behavior (3-request burst, measure timing)
   - Validate field mapping against papers table schema
   - Count available papers for endurance sports query + 2018–2026 filter
3. Append structured findings to docs/api-findings.md
4. Report: what works, what's missing, recommended batch size, any blockers
