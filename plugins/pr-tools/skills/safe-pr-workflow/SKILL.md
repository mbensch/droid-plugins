---
name: safe-pr-workflow
version: 1.0.0
description: |
  Ensures git push and PR operations target the correct branch and don't push to merged/closed PRs.
  Use before any git push, PR creation, or when working across multiple commits in a session.
---

# Safe PR Workflow

## The Problem

When a PR is merged but you continue working on the same branch, subsequent pushes silently update the merged PR's branch on the remote. No new PR is created -- the commits just land on a dead branch. The user sees no PR and has to manually fix things.

## Rules

### Before every `git push`

1. Check if the current branch already has a merged or closed PR:
   ```
   gh pr list --head <current-branch> --state merged --json number,title
   gh pr list --head <current-branch> --state closed --json number,title
   ```

2. If a merged/closed PR exists on this branch, **do not push**. Instead:
   - Create a new branch from the current HEAD
   - Push the new branch
   - Create a fresh PR from the new branch

3. If no merged/closed PR exists, push is safe.

### Before creating a PR with `gh pr create`

1. Run the same check above -- verify the branch doesn't already have a merged/closed PR.
2. If it does, create a new branch first.

### When continuing work after a PR was merged mid-session

If you pushed earlier in the session and the PR was merged, any new commits need a new branch:

```bash
# Check current branch state
gh pr list --head $(git rev-parse --abbrev-ref HEAD) --state all --json number,title,state

# If merged PR found, create new branch from current HEAD
git checkout -b <new-descriptive-branch>
git push -u origin <new-descriptive-branch>
gh pr create --base main ...
```

## What Not To Do

- Never assume a branch is clean for pushing just because `git push` succeeds. A push to a merged PR's branch succeeds silently.
- Never reuse a branch that had a merged PR for new work without creating a fresh branch.
