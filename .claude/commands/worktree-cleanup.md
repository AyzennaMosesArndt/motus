# /worktree-cleanup

Clean up finished worktrees after merge.

## Steps
1. `git worktree list` — show all active worktrees
2. For each worktree not on main/deploy:
   - Check if already merged: `git branch --merged main | grep <branch>`
   - If merged → `git worktree remove <path> --force` + `git branch -d <branch>`
   - If NOT merged → report and skip (never delete unmerged work)
3. Report: removed count, skipped count, remaining worktrees

## Safety rules
- Never remove a worktree with uncommitted changes
- Never remove main or deploy worktrees
- Always confirm before deleting branches

## Manual override
To force-remove a specific worktree:
`git worktree remove .claude/worktrees/<name> --force`
`git branch -D <branch>`  ← only if you're sure
