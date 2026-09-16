#!/usr/bin/env python3
"""Validate supplemental HOSI Research Library sources and contradiction-search records.

This validates structural/provenance relationships only. It does not validate
scientific truth or substitute for human full-text review.
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
PRIMARY_SOURCES = LIB / "sources.json"
SUPPLEMENTAL_SOURCES = LIB / "sources-2026-09-16.json"
CLAIMS = LIB / "claims.json"
SEARCHES = LIB / "contradiction-searches.json"
SEARCH_SCHEMA = LIB / "contradiction-search-record.schema.json"

SOURCE_ID = re.compile(r"^SRC-\d{4}$")
CLAIM_ID = re.compile(r"^CLM-\d{4}$")
SEARCH_ID = re.compile(r"^CSR-\d{4}$")

SOURCE_TYPES = {
    "clinical_guideline", "consensus_statement", "systematic_review", "meta_analysis",
    "randomized_trial", "observational_study", "mechanistic_review", "educational_review",
    "authoritative_government_resource", "other_peer_reviewed",
}
SOURCE_STATES = {"discovered","metadata_verified","full_text_checked","human_reviewed","superseded","retracted","withdrawn"}
SUPERSESSION_STATES = {"current_checked","current_but_older","supersession_check_needed","superseded","unknown"}
RESULTS = {"no_material_conflict_found","mixed_or_qualifying_evidence_found","material_conflict_found","superseded"}
ACTIONS = {"retain_bounded_claim","narrow_claim","hold_claim","supersede_claim","human_review_required_before_state_change"}

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    return None


def iso(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def https(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


schema = load(SEARCH_SCHEMA)
if not isinstance(schema, dict):
    fail("contradiction-search schema must be a JSON object")

primary = load(PRIMARY_SOURCES)
supplemental = load(SUPPLEMENTAL_SOURCES)
claims = load(CLAIMS)
searches = load(SEARCHES)

for name, value in (("sources.json", primary), ("sources-2026-09-16.json", supplemental), ("claims.json", claims), ("contradiction-searches.json", searches)):
    if not isinstance(value, list):
        fail(f"{name} must contain a JSON array")

primary = primary if isinstance(primary, list) else []
supplemental = supplemental if isinstance(supplemental, list) else []
claims = claims if isinstance(claims, list) else []
searches = searches if isinstance(searches, list) else []

all_source_ids: set[str] = set()
for src in primary:
    if isinstance(src, dict) and isinstance(src.get("source_id"), str):
        all_source_ids.add(src["source_id"])

supp_ids: set[str] = set()
required_source = {"source_id","title","source_type","topics","publisher_or_journal","published_year","url","verification_state","verified_on","verified_by","provenance","limitations","supersession_status"}
for idx, src in enumerate(supplemental):
    label = f"supplemental[{idx}]"
    if not isinstance(src, dict):
        fail(f"{label} must be an object")
        continue
    missing = sorted(required_source - set(src))
    if missing:
        fail(f"{label} missing required fields: {', '.join(missing)}")
    sid = src.get("source_id")
    if not isinstance(sid, str) or not SOURCE_ID.fullmatch(sid):
        fail(f"{label} invalid source_id: {sid!r}")
        continue
    if sid in all_source_ids or sid in supp_ids:
        fail(f"duplicate source_id across source shards: {sid}")
    supp_ids.add(sid)
    if src.get("source_type") not in SOURCE_TYPES:
        fail(f"{sid} invalid source_type")
    if src.get("verification_state") not in SOURCE_STATES:
        fail(f"{sid} invalid verification_state")
    if src.get("verification_state") == "human_reviewed":
        fail(f"{sid} supplemental source may not self-assert human_reviewed")
    if src.get("supersession_status") not in SUPERSESSION_STATES:
        fail(f"{sid} invalid supersession_status")
    if not https(src.get("url")):
        fail(f"{sid} must use an https URL")
    if not iso(src.get("verified_on")):
        fail(f"{sid} invalid verified_on")
    if src.get("source_last_updated") is not None and not iso(src.get("source_last_updated")):
        fail(f"{sid} invalid source_last_updated")
    if src.get("next_review_due") is not None and not iso(src.get("next_review_due")):
        fail(f"{sid} invalid next_review_due")
    if not isinstance(src.get("topics"), list) or not src.get("topics"):
        fail(f"{sid} requires at least one topic")
    if not isinstance(src.get("limitations"), list):
        fail(f"{sid} limitations must be an array")

all_source_ids.update(supp_ids)
claim_ids = {c.get("claim_id") for c in claims if isinstance(c, dict) and isinstance(c.get("claim_id"), str)}

search_ids: set[str] = set()
searched_claims: set[str] = set()
required_search = {"search_id","claim_id","searched_on","scope","source_ids","result","summary","human_full_text_review_pending"}
for idx, record in enumerate(searches):
    label = f"contradiction-searches[{idx}]"
    if not isinstance(record, dict):
        fail(f"{label} must be an object")
        continue
    missing = sorted(required_search - set(record))
    if missing:
        fail(f"{label} missing required fields: {', '.join(missing)}")
    search_id = record.get("search_id")
    cid = record.get("claim_id")
    if not isinstance(search_id, str) or not SEARCH_ID.fullmatch(search_id):
        fail(f"{label} invalid search_id: {search_id!r}")
    elif search_id in search_ids:
        fail(f"duplicate search_id: {search_id}")
    else:
        search_ids.add(search_id)
    if not isinstance(cid, str) or not CLAIM_ID.fullmatch(cid) or cid not in claim_ids:
        fail(f"{search_id or label} references unknown/invalid claim_id {cid!r}")
    elif cid in searched_claims:
        fail(f"multiple flagship contradiction-search records for {cid}; consolidate or version explicitly")
    else:
        searched_claims.add(cid)
    if not iso(record.get("searched_on")):
        fail(f"{search_id or label} invalid searched_on")
    if record.get("result") not in RESULTS:
        fail(f"{search_id or label} invalid result")
    if record.get("recommended_claim_action") is not None and record.get("recommended_claim_action") not in ACTIONS:
        fail(f"{search_id or label} invalid recommended_claim_action")
    refs = record.get("source_ids")
    if not isinstance(refs, list) or not refs:
        fail(f"{search_id or label} requires source_ids")
    else:
        for sid in refs:
            if sid not in all_source_ids:
                fail(f"{search_id or label} references unknown source_id {sid!r}")
    if record.get("human_full_text_review_pending") is not True:
        fail(f"{search_id or label} must retain human_full_text_review_pending=true until actual full-text human review is recorded elsewhere")

expected_flagship = {f"CLM-{n:04d}" for n in range(1, 10)}
missing_flagship = sorted(expected_flagship - searched_claims)
if missing_flagship:
    fail(f"missing flagship contradiction searches: {', '.join(missing_flagship)}")

print(f"HOSI contradiction-search QA: {len(supplemental)} supplemental sources, {len(searches)} search records, {len(searched_claims)} flagship claims covered")
if errors:
    for msg in errors:
        print(f"ERROR: {msg}", file=sys.stderr)
    print(f"FAILED: {len(errors)} validation error(s)", file=sys.stderr)
    sys.exit(1)

print("PASS: supplemental source/provenance and contradiction-search relationships are structurally consistent")
print("NOTE: PASS does not mean human full-text review, scientific approval, or curriculum approval occurred.")