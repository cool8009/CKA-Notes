from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


DEFAULT_EXCLUSIONS = {
    "Untitled.md",
    "repo_audit_report.md",
    "context_refresh_log.md",
    "final_repo_update_report.md",
}

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.S)


@dataclass
class Note:
    path: Path
    title: str
    aliases: set[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze wikilink connectivity inside the Obsidian vault."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Vault root. Defaults to the repo root.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="How many unresolved links and weak notes to print.",
    )
    parser.add_argument(
        "--include-root-docs",
        action="store_true",
        help="Include helper/report markdown files in the analysis.",
    )
    return parser.parse_args()


def is_excluded(path: Path, root: Path, include_root_docs: bool) -> bool:
    if ".obsidian" in path.parts:
        return True
    if path.name == "aim routine.md" and path.parent.name == "Images":
        return True
    if not include_root_docs and path.parent == root and path.name in DEFAULT_EXCLUSIONS:
        return True
    return False


def strip_fenced_code_blocks(text: str) -> str:
    lines = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return "\n".join(lines)


def parse_aliases(text: str) -> set[str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return set()

    aliases: set[str] = set()
    lines = match.group(1).splitlines()
    in_aliases = False
    for line in lines:
        alias_match = re.match(r"^aliases:\s*(.*)$", line)
        if alias_match:
            value = alias_match.group(1).strip()
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                if inner:
                    for part in inner.split(","):
                        alias = part.strip().strip("\"'")
                        if alias:
                            aliases.add(alias.lower())
                in_aliases = False
            else:
                in_aliases = value == ""
            continue

        if in_aliases:
            item_match = re.match(r"^\s*-\s*(.+?)\s*$", line)
            if item_match:
                aliases.add(item_match.group(1).strip().strip("\"'").lower())
            elif line.strip() and not line.startswith(" "):
                in_aliases = False
    return aliases


def collect_notes(root: Path, include_root_docs: bool) -> dict[str, Note]:
    notes: dict[str, Note] = {}
    for path in root.rglob("*.md"):
        if is_excluded(path, root, include_root_docs):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        title = path.stem
        notes[title.lower()] = Note(path=path, title=title, aliases=parse_aliases(text))
    return notes


def build_alias_index(notes: dict[str, Note]) -> dict[str, set[str]]:
    index: dict[str, set[str]] = defaultdict(set)
    for note in notes.values():
        index[note.title.lower()].add(note.title)
        for alias in note.aliases:
            index[alias].add(note.title)
    return index


def analyze_links(
    root: Path, notes: dict[str, Note], alias_index: dict[str, set[str]]
) -> tuple[int, Counter[str], dict[str, list[str]], Counter[str], Counter[str]]:
    total_links = 0
    unresolved = Counter()
    unresolved_locations: dict[str, list[str]] = defaultdict(list)
    incoming = Counter()
    outgoing = Counter()

    for note in notes.values():
        text = note.path.read_text(encoding="utf-8", errors="ignore")
        cleaned = strip_fenced_code_blocks(text)
        for lineno, line in enumerate(cleaned.splitlines(), start=1):
            for match in WIKILINK_RE.finditer(line):
                total_links += 1
                target = match.group(1).strip()
                outgoing[note.title] += 1
                matched_titles = alias_index.get(target.lower())
                if matched_titles:
                    for matched in matched_titles:
                        incoming[matched] += 1
                else:
                    unresolved[target] += 1
                    if len(unresolved_locations[target]) < 5:
                        rel = note.path.relative_to(root)
                        unresolved_locations[target].append(f"{rel}:{lineno}")

    return total_links, unresolved, unresolved_locations, incoming, outgoing


def print_report(
    notes: dict[str, Note],
    total_links: int,
    unresolved: Counter[str],
    unresolved_locations: dict[str, list[str]],
    incoming: Counter[str],
    outgoing: Counter[str],
    limit: int,
) -> None:
    resolved_links = total_links - sum(unresolved.values())
    print("Internal Link Analysis")
    print("----------------------")
    print(f"Notes scanned: {len(notes)}")
    print(f"Wikilinks found: {total_links}")
    print(f"Resolved wikilinks: {resolved_links}")
    print(f"Unresolved wikilinks: {sum(unresolved.values())}")
    print()

    print("Top unresolved targets")
    print("----------------------")
    if not unresolved:
        print("None")
    else:
        for target, count in unresolved.most_common(limit):
            locations = ", ".join(unresolved_locations[target])
            print(f"{count:>3}  {target}  ({locations})")
    print()

    weak_notes = []
    for note in notes.values():
        inc = incoming[note.title]
        out = outgoing[note.title]
        weak_notes.append((inc + out, inc, out, note.path.as_posix()))
    weak_notes.sort()

    print("Weakly connected notes")
    print("----------------------")
    for total, inc, out, rel in weak_notes[:limit]:
        print(f"{total:>2} total  {inc:>2} in  {out:>2} out  {rel}")


def main() -> None:
    args = parse_args()
    root = args.root.resolve()
    notes = collect_notes(root, args.include_root_docs)
    alias_index = build_alias_index(notes)
    total_links, unresolved, unresolved_locations, incoming, outgoing = analyze_links(
        root, notes, alias_index
    )
    print_report(
        notes,
        total_links,
        unresolved,
        unresolved_locations,
        incoming,
        outgoing,
        args.limit,
    )


if __name__ == "__main__":
    main()
