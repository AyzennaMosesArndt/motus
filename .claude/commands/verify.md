# /verify

Run the verifier stage standalone — useful for re-checking after schema changes.

## Steps
1. `cd apps/worker`
2. `python pipeline/verifier.py --recheck-all`

## Checks performed
- DOI format valid (regex: 10.\d{4,}/\S+)
- Not already in papers table (deduplication)
- Summary length ≤ 150 words
- At least 1 sport tag assigned
- Evidence level present (1–4)
- No null abstracts slipped through
- Source URL resolves (HEAD request, 200/301/302 acceptable)

## Report
- Total checked
- Passed / failed count
- Failed papers: id + reason
