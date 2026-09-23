#!/usr/bin/env python3
"""Deterministic structural QA for canonical HOSI-101 lesson manuscripts.

This validator intentionally checks structure, provenance/safety markers, and false-finality
language. It does NOT validate scientific truth, citation correctness, clinical safety,
accessibility quality, or human-review completion.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = ROOT / "courses" / "HOSI-101" / "lessons"
LESSON_GLOB = "HOSI101_Lesson_*.md"

REQUIRED_METADATA = (
    "**Status:**",
    "**Lesson ID:**",
    "**Difficulty:**",
    "**Estimated time:**",
    "**Evidence level:**",
    "**Domain tags:**",
    "**Study-path tags:**",
    "**Prerequisites:**",
    "**Revision date:**",
    "**Review state:**",
)

REQUIRED_HEADINGS = (
    "## 1. Original visual / cover",
    "## 2. Why this matters",
    "## 3. Learning objectives",
    "## 4. Vocabulary",
    "## 5. Normal human-system baseline",
    "## 6. Core science",
    "## 7. Historical context",
    "## 8. Evidence map",
    "## 9. What is known",
    "## 10. What is uncertain",
    "## 11. Condition-specific applications",
    "## 12. Combination/comorbidity panel",
    "## 13. Lived-experience perspective",
    "## 14. Practical skill / exercise",
    "## 15. Safety / scope",
    "## 16. Cornell Notes",
    "## 17. Reflection",
    "## 18. Discussion prompt",
    "## 19. Knowledge check / quiz",
    "## 20. Homework",
    "## 21. Instructor answer key / rubric",
    "## 22. References",
    "## 23. Further reading",
    "## 24. Research update log",
    "## 25. What would change our mind?",
)

FORBIDDEN_STATUS_TERMS = (
    "**Status:** Published",
    "**Status:** Reviewed",
    "**Status:** Final",
    "**Status:** Complete",
)

LESSON_ID_RE = re.compile(r"\*\*Lesson ID:\*\*\s+HOSI-101-(\d{3})")
FILENAME_ID_RE = re.compile(r"HOSI101_Lesson_(\d{3})\.md$")


def add_error(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def validate_lesson(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()

    if not text.startswith("# HOSI-101 — Lesson "):
        add_error(errors, path, "missing canonical H1 lesson title")

    for marker in REQUIRED_METADATA:
        if marker not in text:
            add_error(errors, path, f"missing metadata field {marker}")

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            add_error(errors, path, f"missing required section: {heading}")

    for forbidden in FORBIDDEN_STATUS_TERMS:
        if forbidden.lower() in lowered:
            add_error(errors, path, f"false-finality status is not allowed in draft curriculum: {forbidden}")

    status_line = next((line for line in text.splitlines() if line.startswith("**Status:**")), "")
    review_line = next((line for line in text.splitlines() if line.startswith("**Review state:**")), "")
    if "draft" not in status_line.lower():
        add_error(errors, path, "status must explicitly identify the manuscript as a draft")
    if "pending" not in review_line.lower() or "human" not in review_line.lower():
        add_error(errors, path, "review state must explicitly keep independent human review pending")

    if "Original visual brief:" not in text:
        add_error(errors, path, "missing original visual brief")
    if "Accessible alt text:" not in text:
        add_error(errors, path, "missing accessible alt text")

    if "not a diagnosis" not in lowered:
        add_error(errors, path, "Safety / scope must explicitly state that the lesson is not a diagnosis")

    if not re.search(r"\[[A-E](?:/[A-E])?\]", text):
        add_error(errors, path, "no HOSI evidence-confidence marker found in lesson body")

    refs_start = text.find("## 22. References")
    refs_end = text.find("## 23. Further reading")
    if refs_start == -1 or refs_end == -1 or refs_end <= refs_start:
        add_error(errors, path, "references section cannot be parsed")
    else:
        refs = text[refs_start:refs_end]
        if "http" not in refs:
            add_error(errors, path, "references section contains no verifiable URL")

    file_match = FILENAME_ID_RE.search(path.name)
    id_match = LESSON_ID_RE.search(text)
    if not file_match:
        add_error(errors, path, "filename does not contain a three-digit lesson ID")
    elif not id_match:
        add_error(errors, path, "metadata does not contain canonical HOSI-101 lesson ID")
    elif file_match.group(1) != id_match.group(1):
        add_error(
            errors,
            path,
            f"filename ID {file_match.group(1)} does not match metadata ID {id_match.group(1)}",
        )

    return errors


def main() -> int:
    lessons = sorted(LESSON_DIR.glob(LESSON_GLOB))
    if not lessons:
        print(f"ERROR: no canonical lesson files found at {LESSON_DIR / LESSON_GLOB}")
        return 2

    errors: list[str] = []
    seen_ids: set[str] = set()

    for lesson in lessons:
        match = FILENAME_ID_RE.search(lesson.name)
        if match:
            lesson_id = match.group(1)
            if lesson_id in seen_ids:
                add_error(errors, lesson, f"duplicate lesson ID {lesson_id}")
            seen_ids.add(lesson_id)
        errors.extend(validate_lesson(lesson))

    if errors:
        print(f"HOSI-101 curriculum QA FAILED: {len(errors)} issue(s) across {len(lessons)} canonical lesson(s).")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"HOSI-101 curriculum QA PASSED: {len(lessons)} canonical lesson(s) checked.")
    print("Checks: metadata, 25 required sections, draft/human-review state, evidence markers, visual alt text, safety scope, references, and lesson-ID consistency.")
    print("NOTE: passing this validator is NOT scientific, clinical, accessibility, or human-review approval.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
