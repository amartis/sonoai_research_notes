#!/bin/sh
# post-merge hook body (installed by tools/setup_merge.py). The merge driver "index" keeps
# our INDEX.md on a merge, so it misses the other branch's notes. After the merge, regenerate
# INDEX.md and replace the merge commit with one whose tree has the new INDEX.md (same parents,
# message and author; git itself refuses `commit --amend` while the merge is finishing).
top=$(git rev-parse --show-toplevel) || exit 0
cd "$top" || exit 0
python3 tools/build_index.py || { echo "post-merge: build_index.py failed; run it and commit INDEX.md" >&2; exit 0; }
git diff --quiet -- INDEX.md && exit 0
# Rewrite only a merge commit this `git merge` just made: its reflog subject says "Merge made by".
# A fast-forward onto an upstream merge commit ("Fast-forward") must stay as it is.
subject=$(git reflog -1 --format=%gs HEAD 2>/dev/null)
case $subject in
    *"Merge made by"*) parents=$(git rev-list --parents -n 1 HEAD | cut -d' ' -f2-) ;;
    *) parents="" ;;
esac
if [ -z "$parents" ]; then  # fast-forward or squash: no merge commit of ours to fix
    echo "post-merge: INDEX.md regenerated; commit it" >&2
    exit 0
fi
tmp=$(mktemp -u)
trap 'rm -f "$tmp"' EXIT
GIT_INDEX_FILE=$tmp git read-tree HEAD || exit 0
GIT_INDEX_FILE=$tmp git update-index --cacheinfo "100644,$(git hash-object -w INDEX.md),INDEX.md" || exit 0
tree=$(GIT_INDEX_FILE=$tmp git write-tree) || exit 0
args=""
for p in $parents; do args="$args -p $p"; done
new=$(git log -1 --format=%B HEAD | GIT_AUTHOR_NAME=$(git log -1 --format=%an) GIT_AUTHOR_EMAIL=$(git log -1 --format=%ae) \
    GIT_AUTHOR_DATE=$(git log -1 --format=%aI) git commit-tree "$tree" $args) || exit 0
git update-ref -m "post-merge: INDEX.md regenerated" HEAD "$new" && git reset -q -- INDEX.md
echo "post-merge: INDEX.md regenerated into the merge commit"
