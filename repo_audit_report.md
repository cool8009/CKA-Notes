# Repository Audit Report

## Scope

- Phase 1 only.
- This audit is based on the current repo contents.
- For later automation, the safest exclusions are:
  - `Untitled.md` at the repo root, which is the task brief rather than a course note.
  - `Untitled.base`.
  - `04 Application Lifecycle Management/Images/aim routine.md`, which appears unrelated to the CKA notes.
  - Empty placeholder notes unless they are intentionally brought into scope later.

## Repository structure

- Main note folders:
  - `01 Core Concepts`
  - `02 Scheduling`
  - `03 Logging and Monitoring`
  - `04 Application Lifecycle Management`
  - `05 Cluster Maintenance`
  - `06 Security`
  - `Exam Tips`
- Hidden Obsidian config folder:
  - `.obsidian`
- Top-level stray folder:
  - `Untitled 1` (empty)
- Attachment/image folders are local to topic folders rather than centralized:
  - `01 Core Concepts/Images`
  - `02 Scheduling/Images`
  - `04 Application Lifecycle Management/Images`
  - `05 Cluster Maintenance/images`
  - `06 Security/Images`
- Approximate inventory from the current scan:
  - `88` Markdown files total
  - `108` image files total
  - `8` stub/placeholder notes with no body content after frontmatter

## Naming conventions

- Folder names are numbered by study section.
- Note names are mostly human-readable study topics, often prefixed with a number:
  - `00 Cluster Architecture.md`
  - `14 Services - NodePort.md`
  - `20 - Network Policies.md`
- There is mild inconsistency in numbering style:
  - Some sections use zero padding (`00`, `01`, `02`)
  - Others use single digits (`1`, `2`, `3`)
- Filenames frequently contain spaces and some punctuation:
  - hyphens
  - parentheses
  - ampersands
- Image folder casing is inconsistent:
  - most folders use `Images`
  - `05 Cluster Maintenance` uses `images`
- There are placeholder or odd filenames that should be handled cautiously:
  - `01 Core Concepts/Untitled.md`
  - `01 Core Concepts/Untitled 1.md`
  - `01 Core Concepts/21 1Untitled.md`
  - `01 Core Concepts/22 worker node.md`

## Writing conventions

- The repo is primarily a study-note vault, not a polished long-form handbook.
- Tone is conversational and instructional:
  - frequent use of "we", "let's", and direct exam-oriented phrasing
  - many notes read like lesson summaries or self-study prompts
- The dominant body style is bullet-first prose.
- Notes often begin immediately with bullets instead of a top-level heading.
- `##` headings appear when a note needs internal structure, but headings are not mandatory across the repo.
- Code fences are common and usually hold:
  - `kubectl` commands
  - YAML manifests
  - sample command output
- Tables appear occasionally but are not the default layout.
- Callouts do not appear to be a repo convention.
- Some notes are short cheat sheets, while others are longer tutorial-like summaries.
- A small number of notes are stubs with only frontmatter or no content.

## Frontmatter conventions

- YAML frontmatter is common and lightweight.
- Observed pattern:
  - `tags:` is usually present as a YAML list
  - `aliases:` is optional
- `aliases:` appears in both forms:
  - multiline list
  - empty inline array: `aliases: []`
- No strong evidence of broader metadata conventions such as:
  - dates
  - status fields
  - source URLs in frontmatter
  - MOC metadata

## Link conventions

- Internal note links are primarily Obsidian wikilinks.
- Piped wikilinks are used occasionally:
  - `[[12 Multiple Schedulers|multiple schedulers]]`
- Standard Markdown links are present mainly for external resources.
- No local `.md` Markdown links were found.
- There are no established `See also`, `Related`, `Connections`, or `MOC` sections in the current notes.
- Closest things to hub notes are lightweight overview/intro notes such as:
  - `01 Core Concepts/00 Cluster Architecture.md`
  - `05 Cluster Maintenance/01 Intro.md`

## Image and embed conventions

- Local images are mostly embedded with Obsidian-only syntax:
  - `![[Pasted image 20250317190715.png]]`
- Current local image embeds rely on Obsidian name-based attachment resolution rather than explicit relative paths.
- Audit result for local Obsidian image embeds:
  - `101` embeds scanned outside the task brief
  - `101` resolved uniquely to files on disk
  - `0` ambiguous matches
  - `0` missing matches
- Existing standard Markdown images are already in use for remote images:
  - `32` remote Markdown image links found
  - `0` local Markdown image links found outside the task brief
- Several local embeds appear in edge-case formatting that should be normalized carefully during migration:
  - adjacent embeds on one line
  - embeds appended directly to prose
  - embeds attached to bullets without a space

## Likely sources of broken GitHub rendering

- `![[...]]` image embeds are Obsidian-specific and will not render on GitHub.
- Most local image embeds omit the actual folder path and depend on Obsidian's attachment resolution.
- Relative paths will need to account for the note's folder and the actual image folder location.
- Folder-case mismatches matter for GitHub-style paths:
  - `Images` vs `images`
- A few embeds are formatted inline in ways that will become messy if converted mechanically without spacing cleanup.
- Internal wikilinks also do not render as links on GitHub, but that appears to be an intentional repo convention and should be treated as a separate decision from image migration.

## Internal-link graph observations

- The vault already contains meaningful inline wikilinks, especially in `01 Core Concepts`.
- Internal linking is uneven rather than absent:
  - some foundational notes link actively to sibling topics
  - many later notes are mostly standalone
- Several existing wikilinks point to concepts that do not currently have matching note titles or aliases, for example:
  - `[[worker nodes]]`
  - `[[master nodes]]`
  - `[[control plane]]`
  - `[[kubeadm]]`
  - `[[Certificates]]`
- This suggests caution:
  - not every unresolved wikilink is a typo
  - some are intended concept placeholders or shorthand references

## Ambiguous patterns and caution areas

- Do not bulk-rewrite note-to-note links to standard Markdown.
- Do not rename files just to normalize numbering, casing, or punctuation.
- Do not try to "fix" placeholder notes automatically unless there is a clear reason.
- Do not touch remote Markdown images that already render on GitHub.
- Avoid broad text normalization:
  - some notes show pasted-text or encoding artifacts in current content
  - unrelated cleanup would create noisy diffs
- Exclude the task brief and unrelated image-folder note from automated semantic linking.

## Proposed migration rules

### Phase 2 image migration rules

- Only convert local Obsidian image embeds.
- Preserve existing remote Markdown images as-is.
- Resolve each embed against actual files on disk before changing anything.
- Generate standard Markdown image syntax with a correct relative path from the note to the image file.
- URL-encode path characters only where required for Markdown/GitHub safety.
- Preserve readability:
  - if two embeds are adjacent, split them into separate image entries
  - if an embed is glued to prose, move it onto its own line
  - keep surrounding bullets or paragraph structure intact
- Alt text rule set:
  - reuse a clearly descriptive surrounding phrase if one already exists
  - if the filename is descriptive, clean it and use it
  - for `Pasted image ...` files, use a neutral fallback tied to the note context rather than inventing specifics

### Phase 3 internal-link rules

- Keep existing note-to-note links as wikilinks unless there is a strong local reason not to.
- Improve connectivity selectively, not mechanically.
- Favor strong conceptual relationships:
  - prerequisite
  - parent/child
  - sibling comparison
  - follow-up topic
- Prefer light-touch additions:
  - natural inline wikilinks
  - small `Related notes` or `Prerequisites` sections only where they fit the note
- For unresolved existing concept links, prefer one of these approaches:
  - add a fitting alias to an existing note
  - adjust the link target if an obvious existing note already covers the concept
  - leave it alone if the concept does not yet have a justified home

## Recommended implementation approach

- Use a reproducible script with:
  - audit/dry-run mode
  - apply mode
  - validation output
- Keep validation separate from mutation.
- Validation should report at least:
  - unresolved image references
  - any converted image paths that still do not resolve
  - notes skipped for manual review
  - unresolved wikilinks that remain untouched by design

## Suggested next-step plan

1. Build a dry-run resolver for local `![[...]]` image embeds and print the proposed Markdown replacement path for each note.
2. Apply only the safe local image conversions, preserving note layout and remote images.
3. Re-scan the repo for unresolved local image references.
4. Do a second, smaller semantic pass for meaningful internal note links, with special attention to foundational notes and currently weakly connected sections.
