#!/usr/bin/env bash
set -euo pipefail

if [ ! -d "$FACTORY_PROJECT_DIR/.git" ] && ! git -C "$FACTORY_PROJECT_DIR" rev-parse --git-dir >/dev/null 2>&1; then
  exit 0
fi

REPO_NAME=$(basename "$FACTORY_PROJECT_DIR")
WORKTREES_DIR="${FACTORY_PROJECT_DIR}/../droid-worktrees"

if [ ! -d "$WORKTREES_DIR" ]; then
  exit 0
fi

CUTOFF=$(date -v-14d +%s 2>/dev/null || date -d '14 days ago' +%s)

for dir in "$WORKTREES_DIR/${REPO_NAME}"-*; do
  [ -d "$dir" ] || continue

  DIR_MTIME=$(stat -f %m "$dir" 2>/dev/null || stat -c %Y "$dir")
  if [ "$DIR_MTIME" -lt "$CUTOFF" ]; then
    BRANCH=$(git -C "$dir" rev-parse --abbrev-ref HEAD 2>/dev/null || true)
    git -C "$FACTORY_PROJECT_DIR" worktree remove --force "$dir" 2>/dev/null || rm -rf "$dir"
    if [ -n "$BRANCH" ] && echo "$BRANCH" | grep -q '^droid/'; then
      git -C "$FACTORY_PROJECT_DIR" branch -D "$BRANCH" 2>/dev/null || true
    fi
  fi
done
