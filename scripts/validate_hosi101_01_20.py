#!/usr/bin/env python3
"""Deterministic structural QA for HOSI-101 canonical Lessons 001-020.

This validator checks manuscript completeness, status integrity, source/safety markers,
assessment scaffolding, and the exact 20-file block. It does not validate scientific
truth, clinical safety, accessibility quality, or human-review competence.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = ROOT / "courses" / "HOSI-101" / "lessons"
INDEX = LESSON_DIR / "HOSI101_Lessons_01-20.md"
SOURCE_REGISTRY = ROOT / "research" / "HOSI101_Lessons_01-20_SOURCE_REGISTRY.md"
AUDIT = ROOT / "research" / "HOSI101_Lessons_01-20_EVIDENCE_AUDIT_2026-09-16.md"
REVIEW_PACKET = ROOT / "review" / "HOSI101_01-20_HUMAN_REVIEW_PACKET.md"
MANIFEST = ROOT / "courses" / "HOSI-101" / "course-manifest.json"

EXPECTED_IDS = [f"{i:03d}" for i in range(1, 21)]
REVIEW_LESSONS = {"010", "020"}

REQUIRED_METADATA = (
    "**Status:**",
    "**Lesson ID:**",
    "**Module:**",
    "**Difficulty:**",
    "**Estimated time:**",
    "**Evidence level:**",
    "**Domain tags:**",
    "**Study-path tags:**",
    "**Prerequisites:**",
    "**Revision date:**",
    "**Review state:**",
)

SECTION_KEYWORDS = {
    1: ("visual", "cover"),
    2: ("why this matters",),
    3: ("learning objectives",),
    4: ("vocabulary",),
    5: ("baseline",),
    6: ("core",),
    7: (),
    8: ("evidence map",),
    9: ("what is known",),
    10: ("uncertain",),
    11: ("condition",),
    12: ("combination", "comorbidity"),
    13: ("lived",),
    14: ("exercise", "skill"),
    15: ("safety", "scope"),
    16: ("cornell",),
    17: ("reflection",),
    18: ("discussion",),
    19: ("quiz", "knowledge check"),
    20: ("homework",),
    21: ("scholar",),
    22: ("instructor", "rubric", "answer"),
    23: ("references",),
    24: ("further reading",),
    25: ("research update",),
    26: ("what would change our mind",),
}

LESSON_ID_RE = re.compile(r"\*\*Lesson ID:\*\*\s+HOSI-101-(\d{3})")
FILE_RE = re.compile(r"HOSI101_Lesson_(\d{3})\.md$")
SECTION_RE = re.compile(r"^##\s+(\d+)\.\s+(.+)$", re.MULTILINE)
EVIDENCE_RE = re.compile(r"\[[A-E](?:/[A-E])?\]")
URL_RE = re.compile(r"https://")


def fail(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def safety_is_explicit(text: str) -> bool:
    lower = text.lower()
    patterns = (
        r"not\s+(?:a\s+)?diagnos",
        r"does\s+not\s+diagnos",
        r"do\s+not\s+diagnos",
        r"not\s+for\s+diagnos",
        r"not\s+.*diagnostic",
        r"does\s+not\s+.*diagnostic",
    )
    return any(re.search(pattern, lower) for pattern in patterns)


def validate_lesson(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lower = text.lower()

    file_match = FILE_RE.fullmatch(path.name)
    if not file_match:
        fail(errors, path, "invalid canonical lesson filename")
        return errors
    lesson_id = file_match.group(1)

    if not text.startswith("# HOSI-101 — Lesson "):
        fail(errors, path, "missing canonical H1 lesson title")

    for marker in REQUIRED_METADATA:
        if marker not in text:
            fail(errors, path, f"missing metadata field {marker}")

    id_match = LESSON_ID_RE.search(text)
    if not id_match:
        fail(errors, path, "missing canonical Lesson ID metadata")
    elif id_match.group(1) != lesson_id:
        fail(errors, path, f"filename ID {lesson_id} != metadata ID {id_match.group(1)}")

    status = next((line for line in text.splitlines() if line.startswith("**Status:**")), "")
    review = next((line for line in text.splitlines() if line.startswith("**Review state:**")), "")
    if "draft" not in status.lower():
        fail(errors, path, "status must explicitly remain draft")
    if any(word in status.lower() for word in ("published", "final", "complete")):
        fail(errors, path, "draft status contains false-finality language")
    if "human" not in review.lower() or "pending" not in review.lower():
        fail(errors, path, "review state must explicitly keep human review pending")

    sections = {int(n): heading.strip() for n, heading in SECTION_RE.findall(text)}
    if set(sections) != set(range(1, 27)):
        missing = sorted(set(range(1, 27)) - set(sections))
        extra = sorted(set(sections) - set(range(1, 27)))
        if missing:
            fail(errors, path, f"missing numbered section(s): {missing}")
        if extra:
            fail(errors, path, f"unexpected numbered section(s): {extra}")

    for number, keywords in SECTION_KEYWORDS.items():
        heading = sections.get(number, "").lower()
        if keywords and not any(keyword in heading for keyword in keywords):
            fail(errors, path, f"section {number} heading does not match expected role: {sections.get(number)!r}")

    if "visual brief:" not in lower and "original visual brief:" not in lower:
        fail(errors, path, "missing original visual brief")
    if "accessible alt text:" not in lower:
        fail(errors, path, "missing accessible alt text")

    safety_heading = text.find("## 15.")
    cornell_heading = text.find("## 16.")
    safety_text = text[safety_heading:cornell_heading] if safety_heading >= 0 and cornell_heading > safety_heading else ""
    if not safety_is_explicit(safety_text):
        fail(errors, path, "Safety/scope section does not explicitly preserve a non-diagnostic boundary")

    if lesson_id not in REVIEW_LESSONS and not EVIDENCE_RE.search(text):
        fail(errors, path, "no HOSI A-E evidence-confidence marker found")

    refs_start = text.find("## 23.")
    refs_end = text.find("## 24.")
    refs = text[refs_start:refs_end] if refs_start >= 0 and refs_end > refs_start else ""
    if not refs:
        fail(errors, path, "references section cannot be parsed")
    elif not URL_RE.search(refs) and "SOURCE_REGISTRY" not in refs.upper():
        fail(errors, path, "references contain neither an https URL nor a canonical source-registry pointer")

    if "what would change our mind" not in lower:
        fail(errors, path, "missing explicit revision trigger")

    if "homework" not in lower or "knowledge check" not in lower and "quiz" not in lower:
        fail(errors, path, "assessment scaffold is incomplete")

    return errors


def main() -> int:
    errors: list[str] = []

    lessons = sorted(LESSON_DIR.glob("HOSI101_Lesson_*.md"))
    block_lessons = [p for p in lessons if (m := FILE_RE.fullmatch(p.name)) and m.group(1) in EXPECTED_IDS]
    ids = [FILE_RE.fullmatch(p.name).group(1) for p in block_lessons]

    if ids != EXPECTED_IDS:
        missing = [i for i in EXPECTED_IDS if i not in ids]
        duplicates = sorted({i for i in ids if ids.count(i) > 1})
        if missing:
            errors.append(f"canonical 001-020 block missing lesson IDs: {missing}")
        if duplicates:
            errors.append(f"canonical 001-020 block has duplicate IDs: {duplicates}")
        if len(block_lessons) != 20:
            errors.append(f"expected exactly 20 canonical manuscripts for 001-020, found {len(block_lessons)}")

    for lesson in block_lessons:
        errors.extend(validate_lesson(lesson))

    for required in (INDEX, SOURCE_REGISTRY, AUDIT, REVIEW_PACKET, MANIFEST):
        if not required.exists():
            errors.append(f"missing block-level artifact: {required.relative_to(ROOT)}")

    if MANIFEST.exists():
        manifest = MANIFEST.read_text(encoding="utf-8")
        if '"planned_lessons": 200' not in manifest:
            errors.append("course-manifest.json must preserve canonical 200 planned lessons")
        if '"individual_manuscripts": 20' not in manifest:
            errors.append("course-manifest.json must record 20 individual manuscripts for this block")
        if '"publication_state": "not_published"' not in manifest:
            errors.append("course-manifest.json must not imply publication")

    if REVIEW_PACKET.exists():
        review_text = REVIEW_PACKET.read_text(encoding="utf-8")
        if review_text.count("| Pending |") != 20:
            errors.append("human review packet must contain 20 pending per-lesson decisions")
        if "AI output may prepare" not in review_text:
            errors.append("human review packet must explicitly prohibit AI from pre-checking human gates")

    print(f"HOSI-101 Lessons 001-020 QA: {len(block_lessons)} manuscripts inspected")

    if errors:
        print(f"FAILED: {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: exact 20-manuscript block, 26-section architecture, draft/human-review status, visuals, safety, evidence, assessments, references, revision triggers, and block artifacts are structurally consistent.")
    print("NOTE: PASS is not scientific truth, medical clearance, accessibility approval, peer review, publication approval, or human sign-off.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
