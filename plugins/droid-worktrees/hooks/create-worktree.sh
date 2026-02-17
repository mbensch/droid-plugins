#!/usr/bin/env bash
set -euo pipefail

INPUT=$(cat /dev/stdin)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')

if [ ! -d "$FACTORY_PROJECT_DIR/.git" ] && ! git -C "$FACTORY_PROJECT_DIR" rev-parse --git-dir >/dev/null 2>&1; then
  exit 0
fi

REPO_NAME=$(basename "$FACTORY_PROJECT_DIR")
CURRENT_BRANCH=$(git -C "$FACTORY_PROJECT_DIR" rev-parse --abbrev-ref HEAD)
WORKTREE_DIR="${FACTORY_PROJECT_DIR}/../droid-worktrees/${REPO_NAME}-${SESSION_ID}"

if [ -d "$WORKTREE_DIR" ]; then
  echo "Worktree already exists at: ${WORKTREE_DIR} on branch: ${CURRENT_BRANCH}"
  exit 0
fi

NEW_BRANCH="droid/${SESSION_ID}"
git -C "$FACTORY_PROJECT_DIR" worktree add -b "$NEW_BRANCH" "$WORKTREE_DIR" "$CURRENT_BRANCH"

echo "Git worktree created at: ${WORKTREE_DIR} on branch: ${NEW_BRANCH} (based on ${CURRENT_BRANCH}). Work in this worktree."
