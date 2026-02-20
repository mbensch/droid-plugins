---
name: safe-pr-workflow
version: 1.1.0
description: |
  Ensures git push and PR operations target the correct branch and don't push to merged/closed PRs.
  Use before any git push, PR creation, or when working across multiple commits in a session.
---

# Safe PR Workflow

## The Problems

1. **Pushing to a merged branch.** When a PR is merged but you continue working on the same branch, subsequent pushes silently update the merged PR's branch on the remote. No new PR is created -- the commits just land on a dead branch. The user sees no PR and has to manually fix things.

2. **Stale commits leaking into a new PR.** When multiple PRs are created from the same branch over time, earlier commits that were already merged via a previous PR can end up in the new PR's diff. This happens when the branch is not rebased onto the latest base branch before creating the new PR.

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

1. Run the same merged/closed PR check above -- verify the branch doesn't already have a merged/closed PR. If it does, create a new branch first.

2. **Rebase onto the latest base branch** to ensure only the intended commits are in the PR:
   ```bash
   git fetch origin main
   git rebase origin/main
   ```
   After rebasing, verify the commit list is what you expect:
   ```bash
   git log --oneline origin/main..HEAD
   ```
   Every commit listed will appear in the PR. If you see commits that were already merged in a previous PR, the rebase did not complete correctly -- investigate and resolve before pushing.

3. **Force-push with lease** after rebasing to update the remote branch safely:
   ```bash
   git push --force-with-lease origin <branch>
   ```

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

### When reusing a branch for a second PR

If the user creates multiple PRs from the same branch across the session (e.g. the first PR was merged and they kept working):

1. Fetch and rebase onto the base branch **before** pushing or creating the new PR.
2. Confirm with `git log --oneline origin/main..HEAD` that only the new commits are ahead.
3. If stale commits appear, the rebase will typically drop them automatically (git skips already-applied cherry-picks). If not, investigate the conflict.

## What Not To Do

- Never assume a branch is clean for pushing just because `git push` succeeds. A push to a merged PR's branch succeeds silently.
- Never reuse a branch that had a merged PR for new work without creating a fresh branch.
- Never create a PR without first rebasing onto the latest base branch. Skipping the rebase risks including already-merged commits in the new PR's diff.
- Never use `git push --force` -- always use `git push --force-with-lease` to avoid overwriting someone else's work.
