from __future__ import annotations

import argparse
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
ROOT_MAP_NAME = "00 - CKA Notes Map.md"

CHAPTERS = [
    ("01 Core Concepts", "Core Concepts"),
    ("02 Scheduling", "Scheduling"),
    ("03 Logging and Monitoring", "Logging and Monitoring"),
    ("04 Application Lifecycle Management", "Application Lifecycle Management"),
    ("05 Cluster Maintenance", "Cluster Maintenance"),
    ("06 Security", "Security"),
    ("Exam Tips", "Exam Tips"),
]


def natural_key(value: str) -> list[object]:
    parts = re.split(r"(\d+)", value.lower())
    key: list[object] = []
    for part in parts:
        key.append(int(part) if part.isdigit() else part)
    return key


def build_root_map() -> str:
    lines = [
        "- This map connects the main CKA study chapters in this vault.",
        "- It was added to make chapter-to-chapter navigation easier without renaming existing notes.",
        "",
        "## Study Chapters",
    ]
    for folder_name, display_name in CHAPTERS:
        map_name = f"00 - {display_name} Map"
        lines.append(f"- [[{map_name}|{display_name}]]")
    return "\n".join(lines) + "\n"


def build_chapter_map(display_name: str, note_names: list[str]) -> str:
    lines = [
        f'- This map is the main page for the "{display_name}" chapter.',
        "- It groups the notes already in this folder in study order.",
        "",
        "## Notes",
    ]
    for note_name in note_names:
        stem = Path(note_name).stem
        lines.append(f"- [[{stem}]]")
    lines.extend(
        [
            "",
            "## Back To Main Map",
            f"- [[{Path(ROOT_MAP_NAME).stem}|CKA Notes Map]]",
        ]
    )
    return "\n".join(lines) + "\n"


def write_if_changed(path: Path, content: str, apply: bool) -> bool:
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    if existing == content:
        return False
    if apply:
        path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Build root and chapter map pages for the CKA vault.")
    parser.add_argument("--apply", action="store_true", help="Write changes to disk.")
    args = parser.parse_args()

    changes_needed = 0
    chapters_processed = 0

    root_path = REPO_ROOT / ROOT_MAP_NAME
    if write_if_changed(root_path, build_root_map(), args.apply):
        changes_needed += 1

    for folder_name, display_name in CHAPTERS:
        chapter_dir = REPO_ROOT / folder_name
        map_name = f"00 - {display_name} Map.md"
        note_names = sorted(
            [
                path.name
                for path in chapter_dir.glob("*.md")
                if path.name != map_name
            ],
            key=natural_key,
        )
        map_path = chapter_dir / map_name
        if write_if_changed(map_path, build_chapter_map(display_name, note_names), args.apply):
            changes_needed += 1
        chapters_processed += 1

    action = "updated" if args.apply else "would update"
    print(f"chapters processed: {chapters_processed}")
    print(f"map pages to add/update: {changes_needed}")
    print(f"mode: {action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
