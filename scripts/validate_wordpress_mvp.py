#!/usr/bin/env python3
"""Deterministic QA for the HOSI WordPress.com Free campus blueprint.

Checks repository consistency, course/module counts, free-plan honesty, required
publication safeguards, and the static preview's canonical status language.
It cannot verify a deployed WordPress site or current WordPress.com policies.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "platform" / "wordpress-mvp"
MANIFEST = PKG / "SITE_MANIFEST.json"
PREVIEW = ROOT / "platform" / "web" / "mvp" / "index.html"

REQUIRED_FILES = [
    PKG / "README.md",
    MANIFEST,
    PKG / "LESSON_TEMPLATE.md",
    PKG / "BLOCK_PATTERNS.md",
    PKG / "PROGRESS_ASSESSMENT_CERTIFICATES.md",
    PKG / "ACCESSIBILITY_CHECKLIST.md",
    PKG / "PUBLISHING_WORKFLOW.md",
    PKG / "CAMPUS_PAGE_BLUEPRINTS.md",
    PREVIEW,
]

errors: list[str] = []
warnings: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")
        return ""


for path in REQUIRED_FILES:
    if not path.exists():
        fail(f"missing required file: {path.relative_to(ROOT)}")

try:
    manifest = json.loads(text(MANIFEST))
except json.JSONDecodeError as exc:
    fail(f"SITE_MANIFEST.json is invalid JSON: {exc}")
    manifest = {}

if manifest.get("platform_target") != "WordPress.com Free":
    fail("platform_target must remain WordPress.com Free for the $0 MVP")
if manifest.get("deployment_state") != "not_deployed_by_this_manifest":
    fail("manifest must not imply deployment occurred")

course = manifest.get("course", {})
if course.get("course_id") != "HOSI-101":
    fail("manifest course_id must be HOSI-101")
if course.get("planned_lessons") != 200:
    fail("HOSI-101 canonical planned lesson count must be 200")
if course.get("planned_modules") != 20:
    fail("HOSI-101 canonical planned module count must be 20")
if course.get("module_size") != 10:
    fail("HOSI-101 WordPress taxonomy expects 10 lessons per module")

categories = manifest.get("post_categories", [])
module_categories = [c for c in categories if isinstance(c, dict) and c.get("lesson_range")]
if len(module_categories) != 20:
    fail(f"expected 20 module categories, found {len(module_categories)}")

covered: list[int] = []
for index, category in enumerate(module_categories, start=1):
    expected_slug = f"hosi-101-module-{index:02d}"
    if category.get("slug") != expected_slug:
        fail(f"module {index:02d} slug mismatch: {category.get('slug')!r}")
    raw_range = category.get("lesson_range", "")
    match = re.fullmatch(r"(\d+)-(\d+)", raw_range)
    if not match:
        fail(f"module {index:02d} invalid lesson_range: {raw_range!r}")
        continue
    start, end = map(int, match.groups())
    if end - start != 9:
        fail(f"module {index:02d} must contain exactly 10 lesson numbers")
    covered.extend(range(start, end + 1))

if covered and covered != list(range(1, 201)):
    fail("module lesson ranges must cover lessons 1-200 exactly once and in order")

boundaries = manifest.get("free_plan_lms_boundaries", {})
for key in (
    "persistent_individual_progress",
    "authenticated_graded_assessments",
    "automatic_certificate_issuance",
    "private_atlas_storage",
    "plugin_lms",
):
    if boundaries.get(key) is not False:
        fail(f"Free MVP must not claim {key}=true")
for key in ("manual_progress_checklist", "native_self_checks", "search", "category_tag_navigation", "query_loop_course_indexes"):
    if boundaries.get(key) is not True:
        fail(f"Free MVP expected capability missing/false: {key}")

if manifest.get("site_defaults", {}).get("plugin_dependency") is not False:
    fail("Free MVP must not depend on plugins")
if manifest.get("site_defaults", {}).get("sensitive_atlas_collection") is not False:
    fail("Free public WordPress site must not collect sensitive Atlas content")

pages = manifest.get("pages", [])
page_slugs = {p.get("slug") for p in pages if isinstance(p, dict)}
required_page_slugs = {
    "home",
    "start-here",
    "about-hosi",
    "colleges",
    "courses",
    "courses/hosi-101",
    "study-paths",
    "research-library",
    "founders-atlas",
    "evidence-guide",
    "curriculum-status",
    "corrections",
    "policies",
    "accessibility",
    "contact",
}
missing_pages = sorted(required_page_slugs - page_slugs)
if missing_pages:
    fail(f"manifest missing required page slugs: {', '.join(missing_pages)}")

status_vocab = set(manifest.get("public_statuses", []))
required_statuses = {
    "architecture_outline",
    "draft",
    "human_review_pending",
    "reviewed_for_publication",
    "published",
    "correction_pending",
    "superseded",
}
if not required_statuses.issubset(status_vocab):
    fail("public status vocabulary is incomplete")

readme = text(PKG / "README.md")
for required in (
    "WordPress.com Free",
    "1 GB",
    "unlimited pages and posts",
    "plugin",
    "private Atlas",
    "not evidence that a WordPress.com site has already been created or published",
):
    if required.lower() not in readme.lower():
        fail(f"README missing required platform-boundary statement: {required}")

for url in (
    "https://wordpress.com/free/",
    "https://wordpress.com/support/plan-features/",
    "https://wordpress.com/support/plugins/install-a-plugin/",
    "https://wordpress.com/support/domains/set-a-primary-address/",
):
    if url not in readme:
        fail(f"README missing official WordPress.com reference: {url}")

lesson = text(PKG / "LESSON_TEMPLATE.md")
required_lesson_sections = [
    "## Publication metadata",
    "## Why this matters",
    "## Learning objectives",
    "## Normal human-system baseline",
    "## Core science",
    "## Evidence map",
    "## What remains uncertain",
    "## Condition-specific applications",
    "## Combination / comorbidity lens",
    "## Lived-experience perspective",
    "## Safety and scope",
    "## Knowledge check",
    "## Homework",
    "## References",
    "## Research update log",
    "## What would change our mind?",
    "## Corrections",
]
for section in required_lesson_sections:
    if section not in lesson:
        fail(f"LESSON_TEMPLATE missing section: {section}")
if "Personal disclosure is not required" not in lesson:
    fail("LESSON_TEMPLATE must preserve a non-disclosure alternative")
if "does not diagnose" not in lesson.lower():
    fail("LESSON_TEMPLATE must preserve non-diagnostic scope")

progress = text(PKG / "PROGRESS_ASSESSMENT_CERTIFICATES.md")
for phrase in (
    "does not yet store personalized course progress",
    "Certificate of Completion",
    "Do not claim",
    "private Atlas content is not automatically part of the portfolio",
):
    if phrase.lower() not in progress.lower():
        fail(f"progress/certificate policy missing boundary: {phrase}")

blueprints = text(PKG / "CAMPUS_PAGE_BLUEPRINTS.md")
if "View by study path" not in blueprints:
    fail("study-path navigation must be explicitly represented")
if "does not create a diagnostic profile" not in blueprints.lower():
    fail("study-path navigation must preserve non-diagnostic boundary")

publishing = text(PKG / "PUBLISHING_WORKFLOW.md")
for phrase in ("GitHub is the canonical", "Source Git SHA", "Correction pending", "logged-out"):
    if phrase.lower() not in publishing.lower():
        fail(f"publishing workflow missing integrity control: {phrase}")

accessibility = text(PKG / "ACCESSIBILITY_CHECKLIST.md")
for phrase in ("keyboard", "alt text", "mobile", "color alone", "screen-reader", "actual rendered-content testing"):
    if phrase.lower() not in accessibility.lower():
        fail(f"accessibility checklist missing: {phrase}")

preview = text(PREVIEW)
for forbidden in ("300 planned lessons", "Reviewed curriculum foundation", "all 200 lessons are complete"):
    if forbidden.lower() in preview.lower():
        fail(f"static preview contains stale/false status language: {forbidden}")
for required in ("200 planned lessons", "20 modules", "Curriculum development", "human review pending"):
    if required.lower() not in preview.lower():
        fail(f"static preview missing canonical status text: {required}")

# A current capability verification date is useful, but CI cannot itself browse WordPress.com.
verified_date = manifest.get("verified_platform_date")
if not isinstance(verified_date, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", verified_date):
    fail("manifest verified_platform_date must be ISO YYYY-MM-DD")
else:
    warn("WordPress.com capability facts must be re-verified against official docs when platform claims are updated; CI cannot prove web freshness")

print(f"HOSI WordPress MVP QA: {len(pages)} pages, {len(module_categories)} modules, {len(covered)} lesson slots")
for message in warnings:
    print(f"WARNING: {message}")

if errors:
    for message in errors:
        print(f"ERROR: {message}", file=sys.stderr)
    print(f"FAILED: {len(errors)} validation error(s)", file=sys.stderr)
    sys.exit(1)

print("PASS: WordPress campus blueprint consistency checks succeeded")
print("NOTE: PASS does not prove a WordPress site is deployed, accessible in production, reviewed, or LMS-capable.")
