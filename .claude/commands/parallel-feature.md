# /parallel-feature

Spawn parallel subagents to implement a feature in N isolated worktrees.

## Arguments
- FEATURE_NAME (required): e.g. "anatomy-hover-states"
- N (optional, default: 2): number of parallel implementations

## Steps
1. Create N git worktrees:
   ```
   git worktree add .claude/worktrees/<FEATURE_NAME>-1 feature/<FEATURE_NAME>-1
   git worktree add .claude/worktrees/<FEATURE_NAME>-2 feature/<FEATURE_NAME>-2
   ```
2. Spawn N code-generator subagents, one per worktree
3. Each agent implements FEATURE_NAME independently from the same spec
4. When all finish: spawn code-reviewer on each branch
5. Report: diff summary per worktree + reviewer VERDICT per branch
6. Human picks winner → merge to main

## When to use
- Complex UI components (anatomy 3D, feed filters) where multiple approaches make sense
- Performance-sensitive code (pipeline stages) where you want to benchmark alternatives
- Uncertain design decisions — let N agents try, pick the best

## Cleanup after merge
Run /worktree-cleanup
