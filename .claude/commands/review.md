# /review
Spawn code-reviewer agent on current branch.

## Steps
1. Identify current branch: git branch --show-current
2. Spawn code-reviewer agent with scope = changed files since last merge to main
   git diff main...HEAD --name-only
3. Reviewer outputs structured verdict: PASS | NEEDS_CHANGES + findings
4. If PASS: suggest next step (merge to main or /deploy)
5. If NEEDS_CHANGES: list findings with file + line reference
