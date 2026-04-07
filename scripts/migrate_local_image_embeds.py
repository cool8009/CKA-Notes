from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote


ROOT = Path(__file__).resolve().parents[1]
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
EXCLUDED_RELATIVE_PATHS = {
    "Untitled.md",
    "repo_audit_report.md",
}

OBSIDIAN_IMAGE_RE = re.compile(r"!\[\[([^\]]+)\]\]")
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class ResolvedImage:
    raw_target: str
    source: Path
    relative_markdown_path: str


@dataclass
class ReplacementRecord:
    file_path: Path
    raw_embed: str
    replacement: str
    source_image: Path


def iter_note_files(root: Path) -> list[Path]:
    notes: list[Path] = []
    for path in root.rglob("*.md"):
        rel = path.relative_to(root).as_posix()
        if rel.startswith(".obsidian/"):
            continue
        if rel in EXCLUDED_RELATIVE_PATHS:
            continue
        notes.append(path)
    return sorted(notes)


def build_image_indexes(root: Path) -> tuple[dict[str, list[Path]], dict[str, Path]]:
    by_name: dict[str, list[Path]] = defaultdict(list)
    by_relative_path: dict[str, Path] = {}

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        by_name[path.name.lower()].append(path)
        rel_key = path.relative_to(root).as_posix().lower()
        by_relative_path[rel_key] = path

    return by_name, by_relative_path


def encode_markdown_path(path: Path) -> str:
    return "/".join(quote(part, safe=".-_") for part in path.parts)


def clean_display_text(text: str) -> str:
    text = re.sub(r"!\[\[[^\]]+\]\]", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^\s*[-*+]\s*", "", text)
    text = re.sub(r"^\s*\d+\.\s*", "", text)
    text = re.sub(r"[*_`]+", "", text)
    text = text.replace('"', "")
    text = re.sub(r"\s+", " ", text).strip()
    text = text.strip(' "\'`')
    return text.rstrip(" .,:;")


def cleaned_filename_stem(path: Path) -> str:
    stem = path.stem.replace("_", " ").replace("-", " ")
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem


def alt_text_for_embed(
    note_path: Path,
    source_image: Path,
    line_text: str,
    embed_index: int,
) -> str:
    cleaned_line = clean_display_text(line_text)
    if cleaned_line:
        words = cleaned_line.split()
        if len(words) <= 16 and len(cleaned_line) <= 120:
            return cleaned_line

    filename_stem = cleaned_filename_stem(source_image)
    if filename_stem and not filename_stem.lower().startswith("pasted image"):
        return filename_stem

    note_stem = cleaned_filename_stem(note_path)
    if note_stem:
        return f"{note_stem} image {embed_index}"

    return f"Image {embed_index}"


def resolve_embed_target(
    raw_target: str,
    note_path: Path,
    by_name: dict[str, list[Path]],
    by_relative_path: dict[str, Path],
) -> ResolvedImage:
    target = raw_target.strip()
    target = target.split("|", 1)[0].split("#", 1)[0].strip()
    normalized_target = target.replace("\\", "/")

    source_path: Path | None = None
    if "/" in normalized_target:
        source_path = by_relative_path.get(normalized_target.lower())
        if source_path is None:
            leaf = Path(normalized_target).name.lower()
            matches = by_name.get(leaf, [])
            if len(matches) == 1:
                source_path = matches[0]
            elif len(matches) > 1:
                raise ValueError(
                    f"Ambiguous embed target '{raw_target}' in "
                    f"{note_path.relative_to(ROOT).as_posix()}"
                )
    else:
        matches = by_name.get(normalized_target.lower(), [])
        if len(matches) == 1:
            source_path = matches[0]
        elif len(matches) > 1:
            raise ValueError(
                f"Ambiguous embed target '{raw_target}' in "
                f"{note_path.relative_to(ROOT).as_posix()}"
            )

    if source_path is None:
        raise ValueError(
            f"Missing embed target '{raw_target}' in "
            f"{note_path.relative_to(ROOT).as_posix()}"
        )

    relative_path = Path(os.path.relpath(source_path, note_path.parent))
    encoded_path = encode_markdown_path(relative_path)
    return ResolvedImage(raw_target=raw_target, source=source_path, relative_markdown_path=encoded_path)


def transform_note(
    note_path: Path,
    by_name: dict[str, list[Path]],
    by_relative_path: dict[str, Path],
) -> tuple[str, list[ReplacementRecord]]:
    original = note_path.read_text(encoding="utf-8")
    replacements: list[ReplacementRecord] = []
    embed_counter = 0

    def replacement(match: re.Match[str]) -> str:
        nonlocal embed_counter
        embed_counter += 1
        raw_target = match.group(1)
        resolved = resolve_embed_target(raw_target, note_path, by_name, by_relative_path)

        line_start = original.rfind("\n", 0, match.start()) + 1
        line_end = original.find("\n", match.end())
        if line_end == -1:
            line_end = len(original)
        line_text = original[line_start:line_end]

        alt_text = alt_text_for_embed(note_path, resolved.source, line_text, embed_counter)
        markdown_image = f"![{alt_text}]({resolved.relative_markdown_path})"

        prefix = ""
        suffix = ""
        if match.start() > 0:
            before = original[match.start() - 1]
            if before not in {" ", "\t", "\n", "(", "[", "<"}:
                prefix = " "
        if match.end() < len(original):
            after = original[match.end()]
            if after not in {" ", "\t", "\n", ".", ",", ";", ":", "!", "?", ")", "]", ">"}:
                suffix = " "

        replaced = f"{prefix}{markdown_image}{suffix}"
        replacements.append(
            ReplacementRecord(
                file_path=note_path,
                raw_embed=match.group(0),
                replacement=replaced,
                source_image=resolved.source,
            )
        )
        return replaced

    updated = OBSIDIAN_IMAGE_RE.sub(replacement, original)
    updated = re.sub(r"(?m)^(\s*[-*+])(!\[[^\]]*\]\([^)]+\))", r"\1 \2", updated)
    updated = re.sub(r"\)\s{2,}(!\[)", r") \1", updated)
    return updated, replacements


def validate_markdown_images(note_paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for note_path in note_paths:
        text = note_path.read_text(encoding="utf-8")
        for match in MARKDOWN_IMAGE_RE.finditer(text):
            target = match.group(1).strip()
            if re.match(r"^(https?:)?//", target):
                continue
            resolved = (note_path.parent / unquote(target)).resolve()
            if not resolved.exists():
                errors.append(
                    f"Broken markdown image link in {note_path.relative_to(ROOT).as_posix()}: {target}"
                )
        for match in OBSIDIAN_IMAGE_RE.finditer(text):
            errors.append(
                f"Obsidian image embed still present in {note_path.relative_to(ROOT).as_posix()}: {match.group(0)}"
            )
    return errors


def run(apply: bool) -> int:
    note_paths = iter_note_files(ROOT)
    by_name, by_relative_path = build_image_indexes(ROOT)

    changed_files: list[Path] = []
    replacement_records: list[ReplacementRecord] = []
    failures: list[str] = []

    for note_path in note_paths:
        original = note_path.read_text(encoding="utf-8")
        if not OBSIDIAN_IMAGE_RE.search(original):
            continue

        try:
            updated, replacements = transform_note(note_path, by_name, by_relative_path)
        except ValueError as exc:
            failures.append(str(exc))
            continue

        if not replacements:
            continue

        replacement_records.extend(replacements)
        if updated != original:
            changed_files.append(note_path)
            if apply:
                note_path.write_text(updated, encoding="utf-8")

    validation_errors = validate_markdown_images(changed_files if apply else [])

    print(f"Mode: {'apply' if apply else 'dry-run'}")
    print(f"Notes scanned: {len(note_paths)}")
    print(f"Notes with local Obsidian image embeds: {len(changed_files)}")
    print(f"Local Obsidian image embeds processed: {len(replacement_records)}")
    print(f"Resolution failures: {len(failures)}")
    print(f"Validation errors: {len(validation_errors)}")

    if changed_files:
        print("\nChanged notes:")
        for note_path in changed_files:
            print(f"- {note_path.relative_to(ROOT).as_posix()}")

    if replacement_records:
        print("\nSample replacements:")
        for record in replacement_records[:10]:
            rel_note = record.file_path.relative_to(ROOT).as_posix()
            rel_image = record.source_image.relative_to(ROOT).as_posix()
            print(f"- {rel_note}")
            print(f"  {record.raw_embed} -> {record.replacement}")
            print(f"  source: {rel_image}")

    if failures:
        print("\nFailures:")
        for failure in failures:
            print(f"- {failure}")

    if validation_errors:
        print("\nValidation errors:")
        for error in validation_errors:
            print(f"- {error}")

    return 1 if failures or validation_errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert local Obsidian image embeds to standard Markdown image links."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes to disk. Without this flag the script runs in dry-run mode.",
    )
    args = parser.parse_args()
    return run(apply=args.apply)


if __name__ == "__main__":
    sys.exit(main())
