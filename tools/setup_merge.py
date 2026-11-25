#!/usr/bin/env python3
"""One-time setup per clone: merges never need a hand-resolved INDEX.md (TASK-245).

    python tools/setup_merge.py

Sets in this clone (not shared by git, so each clone runs it once):
  - merge driver `index` (used by .gitattributes for INDEX.md): keeps our INDEX.md, no conflict;
  - post-merge hook that runs tools/build_index.py and puts INDEX.md into the merge commit.
Refuses to replace a post-merge hook it did not write. Safe to run again.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARK = "# sonoai-index-merge"
HOOK = f'#!/bin/sh\n{MARK}\nexec "$(git rev-parse --show-toplevel)/tools/post_merge_index.sh"\n'


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True).stdout.strip()


def main() -> int:
    hook = Path(git("rev-parse", "--path-format=absolute", "--git-path", "hooks/post-merge"))
    if hook.exists() and MARK not in hook.read_text():
        print(f"{hook} exists and is not ours; add a call to tools/post_merge_index.sh there by hand", file=sys.stderr)
        return 1
    git("config", "merge.index.name", "keep ours, INDEX.md is regenerated after the merge")
    git("config", "merge.index.driver", "true")
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text(HOOK)
    hook.chmod(0o755)
    print(f"merge driver 'index' set; post-merge hook written to {hook}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
