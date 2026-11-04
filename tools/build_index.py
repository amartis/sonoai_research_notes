#!/usr/bin/env python3
"""Build INDEX.md from the front matter of DIS / DEC / EXP notes, and link IDs in note bodies.

    python tools/build_index.py           # link IDs in note bodies, write INDEX.md
    python tools/build_index.py --check   # exit 1 if anything is stale, unlinked or broken

Standard library only. Front matter is the block between the first two `---`
lines; values are plain strings or `[A, B]` lists, `#` starts a comment.

In each note body (DIS / DEC / EXP, journal, datasets, literature) the first
bare mention of each DIS / DEC / EXP / TASK ID becomes a relative markdown
link; TASK IDs point at the Backlog.md task file in `../backlog/`. Front
matter, fenced code, code spans, existing links, URLs, HTML comments and the
note's own ID are left alone, so a second run changes nothing.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "INDEX.md"
KINDS = {  # prefix -> (folder, heading)
    "DIS": ("discussions", "Discussions"),
    "DEC": ("decisions", "Decisions"),
    "EXP": ("experiments", "Experiments"),
}
BODY_FOLDERS = ("journal", "datasets", "literature")  # other notes whose bodies get links
BACKLOG = ROOT.parent / "backlog"
TASK_FOLDERS = ("tasks", "completed", "archive/tasks")  # where the backlog CLI keeps task files
AREAS = ("data-security", "datasets", "labeling", "training", "workflow", "infra", "aws")  # DEC-040
LINK_FIELDS = ("from", "outcomes", "related", "superseded_by")
ID_RE = re.compile(r"^(DIS|DEC|EXP)-\d{3}$")
MENTION_RE = re.compile(r"(?<![\w-])((?:DIS|DEC|EXP)-\d{3}|TASK-\d{3}(?:\.\d+)?)(?![\w-])")
FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})", re.M)  # any indent, so fences in list items count
NOT_BLANK = r"(?:[^\n]|\n(?![ \t]*\n))"  # any character; a newline only if no blank line follows
SKIP_RE = re.compile(  # inline parts of a body whose IDs are not linked
    rf"(?P<code>(?P<tick>`+){NOT_BLANK}+?(?<!`)(?P=tick)(?!`))"
    rf"|(?P<link>!?\[(?:[^\[\]\n]|\n(?![ \t]*\n)|\[[^\[\]]*\])*\]"
    r"(?:\((?P<target><[^>\n]*>|[^()\s]*)(?:\s+\"[^\"]*\")?\)|\[[^\]]*\]))"
    r"|(?P<refdef>^ {0,3}\[[^\]\n]+\]:[ \t]*(?P<reftarget>\S+)[^\n]*)"
    r"|<!--.*?-->"
    r"|<[A-Za-z][A-Za-z0-9+.-]*:[^>\s]*>"
    r"|https?://\S+",
    re.M | re.S,
)


def split_front_matter(text: str) -> tuple[str, str]:
    """Return (front matter including both `---` lines, body)."""
    if not text.startswith("---"):
        return "", text
    m = re.compile(r"^---[ \t]*$\n?", re.M)
    first = m.match(text)
    close = m.search(text, first.end()) if first else None
    if not close:
        return "", text
    return text[: close.end()], text[close.end():]


def parse_front_matter(path: Path) -> dict | None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    meta: dict = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return meta
        line = line.split(" #", 1)[0].rstrip()
        if not line.strip() or ":" not in line:
            continue
        key, value = (s.strip() for s in line.split(":", 1))
        if value.startswith("[") and value.endswith("]"):
            meta[key] = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        else:
            meta[key] = value
    raise ValueError(f"{path}: front matter not closed")


def links(meta: dict) -> list[str]:
    out = []
    for field in LINK_FIELDS:
        value = meta.get(field) or []
        out += [value] if isinstance(value, str) else value
    return out


def load_notes() -> tuple[dict[str, dict], list[str]]:
    notes, errors = {}, []
    for prefix, (folder, _) in KINDS.items():
        for path in sorted((ROOT / folder).glob(f"{prefix}-*.md")):
            meta = parse_front_matter(path)
            if meta is None:
                errors.append(f"{path.relative_to(ROOT)}: no front matter")
                continue
            nid = meta.get("id", "")
            if not ID_RE.match(nid) or not path.name.startswith(nid + "-"):
                errors.append(f"{path.relative_to(ROOT)}: id {nid!r} does not match file name")
                continue
            if nid in notes:
                errors.append(f"{nid}: duplicate id")
            meta["path"] = path.relative_to(ROOT).as_posix()
            if prefix == "DEC":
                areas = meta.get("area") or []
                areas = [areas] if isinstance(areas, str) else areas
                if not areas:
                    errors.append(f"{nid}: missing area (one or more of {', '.join(AREAS)})")
                for a in areas:
                    if a not in AREAS:
                        errors.append(f"{nid}: unknown area {a!r} (allowed: {', '.join(AREAS)})")
            notes[nid] = meta
    for nid, meta in notes.items():
        for target in links(meta):
            if target not in notes:
                errors.append(f"{nid}: links to unknown {target}")
    return notes, errors


def link_targets(notes: dict[str, dict]) -> dict[str, Path]:
    """Map every linkable ID to its file: notes here, board tasks in ../backlog."""
    targets = {nid: ROOT / m["path"] for nid, m in notes.items()}
    for folder in TASK_FOLDERS:
        for path in sorted((BACKLOG / folder).glob("task-*.md")):
            targets.setdefault(path.name.split(" ", 1)[0].upper(), path)
    return targets


def body_files(notes: dict[str, dict]) -> list[Path]:
    paths = [ROOT / m["path"] for m in notes.values()]
    for folder in BODY_FOLDERS:
        paths += sorted((ROOT / folder).rglob("*.md"))
    return paths


def fenced_blocks(body: str):
    """Yield (start, end) of each fenced code block; an unclosed fence runs to the end."""
    pos = 0
    while m := FENCE_RE.search(body, pos):
        fence = m.group(1)
        close = re.compile(rf"^[ \t]*{re.escape(fence[0])}{{{len(fence)},}}[ \t]*$", re.M)
        line_end = body.find("\n", m.end())
        c = close.search(body, line_end + 1) if line_end >= 0 else None
        end = c.end() if c else len(body)
        yield m.start(), end
        pos = end


def chunks(body: str):
    """Split a body into (kind, text, match): kind is "text", "link" or "skip"."""

    def inline(text: str):
        pos = 0
        for m in SKIP_RE.finditer(text):
            if m.start() > pos:
                yield "text", text[pos:m.start()], None
            yield ("link" if m.group("link") or m.group("refdef") else "skip"), m.group(0), m
            pos = m.end()
        if pos < len(text):
            yield "text", text[pos:], None

    pos = 0
    for start, end in fenced_blocks(body):
        yield from inline(body[pos:start])
        yield "skip", body[start:end], None
        pos = end
    yield from inline(body[pos:])


def relative(target: Path, here: Path) -> str:
    return quote(Path(os.path.relpath(target, here)).as_posix())


def link_body(path: Path, own_id: str | None, targets: dict[str, Path]) -> tuple[str, list[str], list[str]]:
    """Return (text, IDs newly linked, errors) for one note: the first bare mention of each ID gets a link."""
    front, body = split_front_matter(path.read_text(encoding="utf-8"))
    parts = list(chunks(body))
    linked = {own_id} | {nid for kind, text, _ in parts if kind == "link" for nid in MENTION_RE.findall(text)}
    added, errors, out = [], [], []
    name = path.relative_to(ROOT).as_posix()

    def link(m: re.Match) -> str:
        nid = m.group(1)
        if nid in linked:
            return nid
        linked.add(nid)
        if nid not in targets:
            errors.append(f"{name}: mentions unknown {nid} (put it in a code span if that is intended)")
            return nid
        added.append(nid)
        return f"[{nid}]({relative(targets[nid], path.parent)})"

    for kind, text, m in parts:
        if kind == "text":
            text = MENTION_RE.sub(link, text)
        elif kind == "link":
            target = (m.group("target") or m.group("reftarget") or "").strip("<>")
            local = unquote(target.split("#", 1)[0])
            if local and not re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", local) and not (path.parent / local).exists():
                errors.append(f"{name}: broken link {target}")
        out.append(text)
    return front + "".join(out), added, errors


def render(notes: dict[str, dict]) -> str:
    # Reverse links, so each row also shows what came out of it.
    children: dict[str, set[str]] = {nid: set() for nid in notes}
    for nid, meta in notes.items():
        for target in meta.get("from") or []:
            children.setdefault(target, set()).add(nid)
        for target in meta.get("outcomes") or []:
            children[nid].add(target)

    def link(nid: str) -> str:
        return f"[{nid}]({notes[nid]['path']})" if nid in notes else nid

    def link_list(ids) -> str:
        return ", ".join(link(n) for n in ids)

    out = [
        "# Index",
        "",
        "Generated by `tools/build_index.py` from note front matter; do not edit by hand.",
        "",
    ]
    for prefix, (_, heading) in KINDS.items():
        ids = sorted(n for n in notes if n.startswith(prefix))
        if not ids:
            continue
        out += [f"## {heading}", "", "| id | title | status | created | from | leads to | related |",
                "|---|---|---|---|---|---|---|"]
        for nid in ids:
            m = notes[nid]
            status = m.get("status", "")
            if m.get("superseded_by"):
                status += f" by {link(m['superseded_by'])}"
            row = [
                link(nid),
                m.get("title", "").replace("|", "\\|"),
                status,
                m.get("created", ""),
                link_list(m.get("from") or []),
                link_list(sorted(children[nid])),
                link_list(m.get("related") or []),
            ]
            out.append("| " + " | ".join(row) + " |")
        out.append("")

    by_area = {a: sorted(n for n, m in notes.items() if n.startswith("DEC") and m.get("status") == "accepted"
                         and a in ([m["area"]] if isinstance(m.get("area"), str) else m.get("area") or []))
               for a in AREAS}
    out += ["## Accepted decisions by area", "",
            "Accepted DECs only; a decision with two areas is listed under both. "
            "Superseded and proposed ones are in the Decisions table above.", ""]
    for a in AREAS:
        out += [f"### {a}", ""]
        out += [f"- {link(n)}: {notes[n].get('title', '')}" for n in by_area[a]] or ["- none"]
        out.append("")

    edges = sorted({(src, nid) for nid, m in notes.items() for src in m.get("from") or []}
                   | {(nid, dst) for nid, m in notes.items() for dst in m.get("outcomes") or []})
    if edges:
        out += ["## Graph", "", "Arrows follow `from` / `outcomes` (discussion → decision → experiment).", "",
                "```mermaid", "flowchart LR"]
        out += [f"  {a.replace('-', '_')}[{a}] --> {b.replace('-', '_')}[{b}]" for a, b in edges]
        out += ["```", ""]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="verify only, do not write")
    args = ap.parse_args()

    notes, errors = load_notes()
    targets = link_targets(notes)
    own_ids = {ROOT / m["path"]: nid for nid, m in notes.items()}
    relinked = 0
    for path in body_files(notes):
        new, added, errs = link_body(path, own_ids.get(path), targets)
        errors += errs
        if not added:
            continue
        relinked += 1
        if args.check:
            errors.append(f"{path.relative_to(ROOT)}: unlinked {', '.join(added)}; run tools/build_index.py")
        else:
            path.write_text(new, encoding="utf-8")
    text = render(notes)
    if args.check:
        current = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""
        if current != text:
            errors.append("INDEX.md is stale; run tools/build_index.py")
    else:
        INDEX.write_text(text, encoding="utf-8")
        print(f"wrote {INDEX.relative_to(ROOT)} ({len(notes)} notes); linked IDs in {relinked} notes")
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
