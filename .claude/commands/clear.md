# /clear
Full context reset. Use when task is fully done or context is badly polluted.

## Steps
1. Commit any uncommitted changes: git add . && git commit -m "chore: pre-clear checkpoint"
2. Write session summary to CLAUDE.local.md
3. Trigger Claude Code native /clear
Note: use /compact first if you want to preserve session context before clearing.
