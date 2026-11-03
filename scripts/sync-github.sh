#!/usr/bin/env bash
# Sync this theme's tracked files only; never overwrite divergent work.
set -euo pipefail
export GIT_TERMINAL_PROMPT=0
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$root"
test "$(git branch --show-current)" = main
test "$(git remote get-url origin)" = https://github.com/sthuizen/omarchy-biblical-graphite-theme.git
exec 9>"$(git rev-parse --git-path graphite-sync.lock)"
flock -n 9 || exit 0
for operation in MERGE_HEAD CHERRY_PICK_HEAD REVERT_HEAD rebase-merge rebase-apply; do
  if test -e "$(git rev-parse --git-path "$operation")"; then
    echo "Git operation in progress; sync deferred." >&2
    exit 1
  fi
done
git fetch origin main
if ! git merge-base --is-ancestor origin/main HEAD; then
  if git merge-base --is-ancestor HEAD origin/main && test -z "$(git status --porcelain)"; then
    git merge --ff-only origin/main
  else
    echo "Local work and GitHub need reconciliation; no files overwritten." >&2
    exit 1
  fi
fi
git add -u
if ! git diff --cached --quiet; then
  git diff --cached --check
  git commit -m "Sync Biblical Graphite theme changes"
fi
git push origin main
local_head=$(git rev-parse HEAD)
remote_head=$(git ls-remote origin refs/heads/main | cut -f1)
test "$local_head" = "$remote_head"
echo "Biblical Graphite synced: $local_head"
