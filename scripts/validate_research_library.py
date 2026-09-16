#!/usr/bin/env python3
"""Deterministic structural validator for the HOSI Research Library MVP.

This validates repository structure, IDs, state transitions, provenance links,
and basic metadata hygiene. It does NOT validate scientific truth, clinical
accuracy, evidence quality, or human-review competence.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "research" / "library"

SOURCE_FILE = LIB / "sources.json"
CLAIM_FILE = LIB / "claims.json"
REVIEW_FILE = LIB / "review-events.json"
SCHEMA_FILES = [
    LIB / "source-record.schema.json",
    LIB / "claim-record.schema.json",
    LIB / "review-event.schema.json",
]

SOURCE_ID = re.compile(r"^SRC-\d{4}$")
CLAIM_ID = re.compile(r"^CLM-\d{4}$")
REVIEW_ID = re.compile(r"^REV-\d{4}$")

SOURCE_TYPES = {
    "clinical_guideline",
    "consensus_statement",
    "systematic_review",
    "meta_analysis",
    "randomized_trial",
    "observational_study",
    "mechanistic_review",
    "educational_review",
    "authoritative_government_resource",
    "other_peer_reviewed",
}

SOURCE_STATES = {
    "discovered",
    "metadata_verified",
    "full_text_checked",
    "human_reviewed",
    "superseded",
    "retracted",
    "withdrawn",
}

SUPERSESSION_STATES = {
    "current_checked",
    "current_but_older",
    "supersession_check_needed",
    "superseded",
    "unknown",
}

CLAIM_STATES = {
    "draft",
    "source_matched",
    "contradiction_searched",
    "human_reviewed",
    "approved_for_curriculum",
    "held",
    "superseded",
}

CONTRADICTION_STATES = {
    "not_searched",
    "searched_none_material_found",
    "material_conflict_found",
    "mixed_evidence",
}

REVIEW_ROLES = {
    "subject_matter",
    "clinical_safety",
    "lived_experience",
    "accessibility",
    "assessment",
    "editorial",
    "other",
}

REVIEW_DECISIONS = {
    "approve_for_next_gate",
    "approve_with_non_blocking_corrections",
    "revise_and_re_review",
    "hold",
}

SOURCE_REQUIRED = {
    "source_id",
    "title",
    "source_type",
    "topics",
    "publisher_or_journal",
    "published_year",
    "url",
    "verification_state",
    "verified_on",
    "verified_by",
    "provenance",
    "limitations",
    "supersession_status",
}

CLAIM_REQUIRED = {
    "claim_id",
    "claim",
    "domain",
    "population",
    "evidence_rating",
    "source_ids",
    "what_evidence_establishes",
    "what_evidence_does_not_establish",
    "contradictory_evidence",
    "applicability",
    "status",
    "reviewed_on",
    "reviewed_by",
    "revision_history",
}

REVIEW_REQUIRED = {
    "review_event_id",
    "reviewer_name",
    "reviewer_role",
    "expertise_or_perspective",
    "conflict_of_interest",
    "review_date",
    "reviewed_source_ids",
    "reviewed_claim_ids",
    "decision",
    "notes",
    "repository_commit",
}


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def valid_iso_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def valid_https_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def missing_keys(record: dict, required: set[str]) -> list[str]:
    return sorted(k for k in required if k not in record)


errors: list[str] = []
warnings: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


# Ensure schema documents themselves remain parseable JSON.
for schema_path in SCHEMA_FILES:
    schema = load_json(schema_path)
    if not isinstance(schema, dict):
        fail(f"schema is not a JSON object: {schema_path.relative_to(ROOT)}")

sources = load_json(SOURCE_FILE)
claims = load_json(CLAIM_FILE)
reviews = load_json(REVIEW_FILE)

if not isinstance(sources, list):
    fail("sources.json must contain a JSON array")
    sources = []
if not isinstance(claims, list):
    fail("claims.json must contain a JSON array")
    claims = []
if not isinstance(reviews, list):
    fail("review-events.json must contain a JSON array")
    reviews = []

source_ids: set[str] = set()
claim_ids: set[str] = set()
review_ids: set[str] = set()

for index, src in enumerate(sources):
    label = f"sources[{index}]"
    if not isinstance(src, dict):
        fail(f"{label} must be an object")
        continue

    missing = missing_keys(src, SOURCE_REQUIRED)
    if missing:
        fail(f"{label} missing required fields: {', '.join(missing)}")

    sid = src.get("source_id")
    if not isinstance(sid, str) or not SOURCE_ID.fullmatch(sid):
        fail(f"{label} has invalid source_id: {sid!r}")
    elif sid in source_ids:
        fail(f"duplicate source_id: {sid}")
    else:
        source_ids.add(sid)

    if src.get("source_type") not in SOURCE_TYPES:
        fail(f"{sid or label} has invalid source_type: {src.get('source_type')!r}")
    if src.get("verification_state") not in SOURCE_STATES:
        fail(f"{sid or label} has invalid verification_state: {src.get('verification_state')!r}")
    if src.get("supersession_status") not in SUPERSESSION_STATES:
        fail(f"{sid or label} has invalid supersession_status: {src.get('supersession_status')!r}")
    if not valid_https_url(src.get("url")):
        fail(f"{sid or label} must use a valid https URL")
    if not valid_iso_date(src.get("verified_on")):
        fail(f"{sid or label} has invalid verified_on date")
    if src.get("source_last_updated") is not None and not valid_iso_date(src.get("source_last_updated")):
        fail(f"{sid or label} has invalid source_last_updated date")
    if src.get("next_review_due") is not None and not valid_iso_date(src.get("next_review_due")):
        fail(f"{sid or label} has invalid next_review_due date")
    if not isinstance(src.get("topics"), list) or not src.get("topics"):
        fail(f"{sid or label} must contain at least one topic")
    if not isinstance(src.get("limitations"), list):
        fail(f"{sid or label} limitations must be an array")

    if src.get("verification_state") == "human_reviewed":
        # Cross-checked after review registry is parsed.
        pass

    if src.get("supersession_status") == "superseded" and not src.get("superseded_by"):
        fail(f"{sid or label} is superseded but has no superseded_by source ID")

    if isinstance(src.get("published_year"), int) and src["published_year"] < 2010:
        if src.get("supersession_status") == "current_checked":
            warn(f"{sid}: older source marked current_checked; verify supersession search is documented")

for index, claim in enumerate(claims):
    label = f"claims[{index}]"
    if not isinstance(claim, dict):
        fail(f"{label} must be an object")
        continue

    missing = missing_keys(claim, CLAIM_REQUIRED)
    if missing:
        fail(f"{label} missing required fields: {', '.join(missing)}")

    cid = claim.get("claim_id")
    if not isinstance(cid, str) or not CLAIM_ID.fullmatch(cid):
        fail(f"{label} has invalid claim_id: {cid!r}")
    elif cid in claim_ids:
        fail(f"duplicate claim_id: {cid}")
    else:
        claim_ids.add(cid)

    if claim.get("evidence_rating") not in {"A", "B", "C", "D", "E"}:
        fail(f"{cid or label} has invalid evidence_rating")
    if claim.get("status") not in CLAIM_STATES:
        fail(f"{cid or label} has invalid status: {claim.get('status')!r}")
    if not valid_iso_date(claim.get("reviewed_on")):
        fail(f"{cid or label} has invalid reviewed_on date")

    source_refs = claim.get("source_ids")
    if not isinstance(source_refs, list) or not source_refs:
        fail(f"{cid or label} must reference at least one source")
    else:
        for sid in source_refs:
            if sid not in source_ids:
                fail(f"{cid or label} references unknown source_id {sid!r}")

    contradiction = claim.get("contradictory_evidence")
    if not isinstance(contradiction, dict):
        fail(f"{cid or label} contradictory_evidence must be an object")
    else:
        cstate = contradiction.get("status")
        if cstate not in CONTRADICTION_STATES:
            fail(f"{cid or label} has invalid contradiction status: {cstate!r}")
        for sid in contradiction.get("source_ids", []):
            if sid not in source_ids:
                fail(f"{cid or label} contradiction section references unknown source_id {sid!r}")

    history = claim.get("revision_history")
    if not isinstance(history, list) or not history:
        fail(f"{cid or label} requires non-empty revision_history")
    else:
        for hindex, event in enumerate(history):
            if not isinstance(event, dict):
                fail(f"{cid or label} revision_history[{hindex}] must be an object")
                continue
            for field in ("date", "change", "by"):
                if field not in event:
                    fail(f"{cid or label} revision_history[{hindex}] missing {field}")
            if "date" in event and not valid_iso_date(event.get("date")):
                fail(f"{cid or label} revision_history[{hindex}] has invalid date")

    if claim.get("status") in {"human_reviewed", "approved_for_curriculum"} and not claim.get("human_reviewer"):
        fail(f"{cid or label} cannot be {claim.get('status')} without human_reviewer")

for index, review in enumerate(reviews):
    label = f"review-events[{index}]"
    if not isinstance(review, dict):
        fail(f"{label} must be an object")
        continue

    missing = missing_keys(review, REVIEW_REQUIRED)
    if missing:
        fail(f"{label} missing required fields: {', '.join(missing)}")

    rid = review.get("review_event_id")
    if not isinstance(rid, str) or not REVIEW_ID.fullmatch(rid):
        fail(f"{label} has invalid review_event_id: {rid!r}")
    elif rid in review_ids:
        fail(f"duplicate review_event_id: {rid}")
    else:
        review_ids.add(rid)

    if review.get("reviewer_role") not in REVIEW_ROLES:
        fail(f"{rid or label} has invalid reviewer_role")
    if review.get("decision") not in REVIEW_DECISIONS:
        fail(f"{rid or label} has invalid decision")
    if not valid_iso_date(review.get("review_date")):
        fail(f"{rid or label} has invalid review_date")

    for sid in review.get("reviewed_source_ids", []):
        if sid not in source_ids:
            fail(f"{rid or label} references unknown source_id {sid!r}")
    for cid in review.get("reviewed_claim_ids", []):
        if cid not in claim_ids:
            fail(f"{rid or label} references unknown claim_id {cid!r}")

# Human-reviewed states require an actual human review event referencing the record.
reviewed_sources = {
    sid
    for review in reviews
    for sid in review.get("reviewed_source_ids", [])
    if isinstance(review, dict)
}
reviewed_claims = {
    cid
    for review in reviews
    for cid in review.get("reviewed_claim_ids", [])
    if isinstance(review, dict)
}

for src in sources:
    if isinstance(src, dict) and src.get("verification_state") == "human_reviewed":
        sid = src.get("source_id")
        if sid not in reviewed_sources:
            fail(f"{sid} marked human_reviewed without a corresponding review event")

for claim in claims:
    if not isinstance(claim, dict):
        continue
    cid = claim.get("claim_id")
    if claim.get("status") in {"human_reviewed", "approved_for_curriculum"} and cid not in reviewed_claims:
        fail(f"{cid} marked {claim.get('status')} without a corresponding review event")

# A claim cannot say contradiction search is complete while retaining source-matched status only.
for claim in claims:
    if not isinstance(claim, dict):
        continue
    contradiction = claim.get("contradictory_evidence", {})
    cstate = contradiction.get("status") if isinstance(contradiction, dict) else None
    if cstate != "not_searched" and claim.get("status") == "source_matched":
        warn(f"{claim.get('claim_id')}: contradiction search recorded but claim status remains source_matched")

print(f"HOSI Research Library QA: {len(sources)} sources, {len(claims)} claims, {len(reviews)} human review events")
for message in warnings:
    print(f"WARNING: {message}")

if errors:
    for message in errors:
        print(f"ERROR: {message}", file=sys.stderr)
    print(f"FAILED: {len(errors)} validation error(s)", file=sys.stderr)
    sys.exit(1)

print("PASS: structural/provenance validation succeeded")
print("NOTE: PASS does not mean scientific, clinical, accessibility, or human-review approval.")
