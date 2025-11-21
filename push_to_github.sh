#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PRIMARY_GIT_DIR="$ROOT_DIR/.git"
ALT_GIT_DIR="$ROOT_DIR/.git-data/repo"
TMP_GIT="/tmp/tryon-git"

if [ ! -d "$ALT_GIT_DIR" ] && [ -d "$TMP_GIT" ]; then
  echo "Git metadata cache not found. Copying from $TMP_GIT..."
  mkdir -p "$(dirname "$ALT_GIT_DIR")"
  cp -R "$TMP_GIT" "$ALT_GIT_DIR"
fi

if [ -d "$PRIMARY_GIT_DIR" ]; then
  export GIT_DIR="$PRIMARY_GIT_DIR"
  export GIT_WORK_TREE="$ROOT_DIR"
elif [ -d "$ALT_GIT_DIR" ]; then
  export GIT_DIR="$ALT_GIT_DIR"
  export GIT_WORK_TREE="$ROOT_DIR"
else
  echo "Error: no git metadata found in .git or .git-data." >&2
  exit 1
fi

if [ $# -eq 0 ]; then
  echo "Using default message: 'Auto update'"
  COMMIT_MESSAGE="Auto update"
else
  COMMIT_MESSAGE="$*"
fi

echo "Adding changes..."
git add -A

if git diff --quiet --cached; then
  echo "No changes to commit."
  exit 0
fi

echo "Committing changes..."
git commit -m "$COMMIT_MESSAGE"

echo "Pushing to GitHub..."
git push origin main

echo "Done!"
