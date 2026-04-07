You are working locally inside my Obsidian notes repository, which is also version-controlled in GitHub.

Your job is to do this in **three explicit phases**, in order, and be careful not to make blind bulk edits.

## Overall goals

* Read the repo first and understand it before changing anything.
* Preserve the repository’s existing writing style, structure, and note-taking conventions unless there is a strong reason to normalize something.
* Make image links work in both **Obsidian Markdown** and **GitHub Markdown**.
* Improve the internal note-linking / “mind map” quality of the notes by adding meaningful connections between related notes.
* Prefer **standard Markdown** where possible, but do not damage Obsidian usability.
* Make all changes reviewable and deterministic.
* Be conservative. Do not invent facts or content not supported by the existing notes.

---

# Phase 1 — Repository audit and conventions analysis

First, inspect the repository before changing any files.

## In this phase, do all of the following:

1. Discover the repo structure:

   * main note folders
   * attachment / image folders
   * index / MOC / hub notes
   * templates
   * any frontmatter conventions
   * naming conventions for files and folders
   * how links are currently written
   * whether there are spaces, special characters, or inconsistent casing in filenames

2. Read a representative sample of notes from different folders and infer the writing conventions, including:

   * heading style
   * paragraph style
   * bullet/list style
   * use of bold / italics / callouts
   * use of frontmatter
   * use of tags
   * use of wikilinks vs standard markdown links
   * use of embedded images
   * use of “See also”, “Related”, “MOC”, “Connections”, or similar sections
   * tone and level of formality
   * whether notes are atomic, long-form, tutorial-like, diary-like, study notes, etc.

3. Produce a short audit note/report that summarizes:

   * repo structure
   * observed writing conventions
   * link conventions
   * image/embed conventions
   * likely sources of broken GitHub rendering
   * proposed migration rules
   * ambiguous patterns that need caution

## Important constraints for Phase 1

* Do not modify notes yet unless you must generate a separate audit report file.
* If you generate a report, place it in a clearly named file such as `repo_audit_report.md`.
* Base your conventions on what is actually in the repo, not assumptions.

---

# Phase 2 — Fix image links for both Obsidian and GitHub

After the audit, go through the notes and fix image links so they render correctly in both Obsidian and GitHub.

## Main objective

Replace or normalize image embeds so that:

* GitHub can render them
* Obsidian still works well
* relative paths are correct from the location of each note
* case-sensitive path issues are handled correctly

## Do all of the following:

1. Detect all image embed patterns, including examples like:

   * `![[image.png]]`
   * `![[folder/image.png]]`
   * `![](relative/path.png)`
   * any malformed or partially broken markdown image syntax

2. Resolve each image reference to the actual file on disk.

3. Convert Obsidian-only image embeds into a format that works in GitHub Markdown, preferably:

   * `![alt text](relative/path.png)`

4. Choose alt text intelligently:

   * if an image name is descriptive, use a cleaned-up version of the filename
   * if surrounding text provides a better label, use that
   * otherwise use a simple safe fallback

5. Fix relative paths so they are correct from each note’s directory.

6. Handle edge cases carefully:

   * spaces in filenames
   * URL encoding when needed
   * case mismatches between link and actual filename
   * duplicate filenames in different folders
   * attachments stored in central vs local folders
   * images referenced with missing extensions

7. Preserve note readability.

   * Do not clutter notes with ugly unnecessary transformations.
   * Keep formatting clean.

8. Create a validation pass that checks:

   * broken image links after migration
   * unresolved image references
   * duplicate / ambiguous matches
   * files needing manual review

## Important constraints for Phase 2

* Do not move or rename files unless necessary.
* If renaming or moving is necessary, do it minimally and document it clearly.
* Prefer updating links over changing the file system.
* Keep changes diff-friendly.

---

# Phase 3 — Create proper mind map connections in the text

After image links are fixed, do a second semantic pass over the notes and improve the internal knowledge graph by adding meaningful links between related notes.

## Main objective

Create better “mind map” connectivity in the notes themselves, not just random extra links.

## In this phase, do all of the following:

1. Analyze note topics and relationships:

   * parent/child concepts
   * prerequisite concepts
   * related sibling topics
   * contrasting topics
   * follow-up / next-step topics
   * concept clusters that should be cross-linked

2. Add internal links where they genuinely improve navigation and understanding.

3. Follow the repo’s existing writing conventions from Phase 1:

   * if the repo uses `[[Wikilinks]]`, preserve or prefer that for note-to-note links unless standard markdown is clearly better
   * if the repo uses sections like “Related notes” / “See also” / “Connections”, use them consistently
   * if connections are usually inline in prose, add them inline naturally

4. Create or improve “mind map” style structures where useful:

   * MOC / index notes
   * “Related notes” sections
   * “Prerequisites” sections
   * “See also” sections
   * hub notes for clusters of related notes
   * backlink-friendly links between conceptually connected notes

5. Be selective:

   * avoid spammy overlinking
   * do not link every mention of a term
   * prioritize strong conceptual relationships

6. Preserve author voice:

   * do not rewrite the entire repository just to insert links
   * lightly edit surrounding text only when needed to make links read naturally

7. Identify orphan notes and weakly connected notes, and improve their connectivity where justified.

## Important constraints for Phase 3

* Do not invent knowledge that is not already supported by the repo.
* Do not add fake structure where the content does not justify it.
* Do not create noisy “SEO-like” internal linking.
* Links should feel like a thoughtful knowledge system, not automation spam.

---

# Implementation requirements

## Before making large changes

* Create a clear migration plan based on the audit.
* Explain the plan briefly in a report or terminal output before applying changes.

## During implementation

* Use scripts where appropriate, preferably Python.
* Make the process reproducible.
* Prefer:

  * an audit step
  * a dry-run mode
  * an apply mode
  * a final validation/report step

## After all changes

Produce a final summary report that includes:

1. What conventions were detected
2. What image-link transformations were made
3. What mind-map/internal-link improvements were made
4. Which files were changed
5. Which files need manual review
6. Any ambiguities or unresolved cases
7. Validation results:

   * broken image links remaining
   * broken internal note links remaining
   * orphan notes remaining
   * duplicate / ambiguous note titles if relevant

---

# Quality bar

* Read first, then act.
* Be conservative, precise, and reviewable.
* Preserve existing style.
* Improve compatibility and connectivity without making the repo feel machine-generated.

Start with Phase 1 only: inspect the repo, infer conventions, and propose the migration plan before performing broad edits.
