#!/usr/bin/env python3
"""Deterministic governance QA for HOSI review/public-beta gates.

This validator checks structural consistency and prevents automated status inflation.
It cannot perform human subject-matter, medical, lived-experience, accessibility,
privacy/security, learner-pilot, or release review.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review"
GATES = REVIEW / "PUBLIC_BETA_GATES.json"
EVENTS = REVIEW / "review-events.json"
CORRECTIONS = REVIEW / "corrections.json"

REQUIRED = [
    REVIEW / "README.md",
    GATES,
    REVIEW / "review-event.schema.json",
    EVENTS,
    REVIEW / "REVIEW_PACKETS.md",
    REVIEW / "AI_RED_TEAM.md",
    REVIEW / "LEARNER_PILOT.md",
    REVIEW / "correction-record.schema.json",
    CORRECTIONS,
    REVIEW / "PUBLIC_BETA_CHECKLIST.md",
    REVIEW / "RELEASE_POLICY.md",
]

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    return None


def normalize_markdown(value: str) -> str:
    """Normalize simple Markdown emphasis so policy checks test meaning, not styling."""
    value = value.replace("**", "").replace("__", "")
    value = value.replace("`", "")
    return re.sub(r"\s+", " ", value).strip()


for path in REQUIRED:
    if not path.exists():
        fail(f"missing required file: {path.relative_to(ROOT)}")

manifest = load_json(GATES) or {}
events = load_json(EVENTS)
corrections = load_json(CORRECTIONS)

if not isinstance(events, list):
    fail("review-events.json must be an array")
    events = []
if not isinstance(corrections, list):
    fail("corrections.json must be an array")
    corrections = []

if manifest.get("release_state") != "not_approved":
    fail("initial public-beta governance branch must remain release_state=not_approved")
if manifest.get("human_release_decision_required") is not True:
    fail("human_release_decision_required must be true")
if manifest.get("ci_can_approve_release") is not False:
    fail("CI must never be able to approve release")
if manifest.get("final_label_allowed_without_human_release_event") is not False:
    fail("final label must require a human release event")

gates = manifest.get("gates", [])
if len(gates) != 12:
    fail(f"expected 12 governance gates, found {len(gates)}")

gate_ids: set[str] = set()
gate_map: dict[str, dict] = {}
for gate in gates:
    gate_id = gate.get("gate_id")
    if not isinstance(gate_id, str) or not re.fullmatch(r"GATE-\d{2}", gate_id):
        fail(f"invalid gate ID: {gate_id!r}")
        continue
    if gate_id in gate_ids:
        fail(f"duplicate gate ID: {gate_id}")
    gate_ids.add(gate_id)
    gate_map[gate_id] = gate
    if gate.get("status") not in {"not_started","in_progress","changes_required","passed","not_applicable"}:
        fail(f"invalid status for {gate_id}: {gate.get('status')!r}")

expected_names = {
    "subject_matter_review",
    "citation_claim_source_audit",
    "medical_safety_review",
    "lived_experience_review",
    "accessibility_review",
    "assessment_rubric_review",
    "privacy_security_review",
    "ai_red_team",
    "learner_pilot",
    "correction_resolution",
    "automated_qa",
    "explicit_human_release_decision",
}
if {g.get("name") for g in gates} != expected_names:
    fail("gate-name set does not match required public-beta governance gates")

human_only_ids = {g["gate_id"] for g in gates if g.get("human_only") is True}

review_ids: set[str] = set()
for event in events:
    review_id = event.get("review_id")
    gate_id = event.get("gate_id")
    if not isinstance(review_id, str) or not re.fullmatch(r"REV-\d{4}", review_id):
        fail(f"invalid review_id: {review_id!r}")
    elif review_id in review_ids:
        fail(f"duplicate review_id: {review_id}")
    else:
        review_ids.add(review_id)
    if gate_id not in gate_map:
        fail(f"review event {review_id!r} references unknown gate {gate_id!r}")
    if not event.get("version_ref"):
        fail(f"review event {review_id!r} missing version_ref")
    if event.get("decision") not in {"pass","pass_with_nonblocking_notes","changes_required","reject","not_applicable"}:
        fail(f"review event {review_id!r} has invalid decision")

for gate_id in human_only_ids:
    gate = gate_map.get(gate_id, {})
    if gate.get("status") == "passed":
        matching = [e for e in events if e.get("gate_id") == gate_id and e.get("decision") in {"pass","pass_with_nonblocking_notes"}]
        if not matching:
            fail(f"human-only {gate_id} cannot be passed without a matching human review event")

release_gate = next((g for g in gates if g.get("name") == "explicit_human_release_decision"), None)
if release_gate and release_gate.get("status") == "passed":
    matching = [e for e in events if e.get("gate_id") == release_gate.get("gate_id") and e.get("reviewer_role") == "release_authority" and e.get("decision") in {"pass","pass_with_nonblocking_notes"}]
    if not matching:
        fail("release gate cannot pass without an authorized human release event")

correction_ids: set[str] = set()
for record in corrections:
    correction_id = record.get("correction_id")
    if not isinstance(correction_id, str) or not re.fullmatch(r"COR-\d{4}", correction_id):
        fail(f"invalid correction_id: {correction_id!r}")
    elif correction_id in correction_ids:
        fail(f"duplicate correction_id: {correction_id}")
    else:
        correction_ids.add(correction_id)
    if record.get("status") not in {"open","in_progress","resolved_pending_review","closed","wont_fix_with_rationale"}:
        fail(f"correction {correction_id!r} has invalid status")

critical_open = [c for c in corrections if c.get("severity") == "critical" and c.get("status") not in {"closed","wont_fix_with_rationale"}]
if manifest.get("release_state") != "not_approved" and critical_open:
    fail("release cannot advance while critical corrections are open")

checklist = (REVIEW / "PUBLIC_BETA_CHECKLIST.md").read_text(encoding="utf-8") if (REVIEW / "PUBLIC_BETA_CHECKLIST.md").exists() else ""
plain_checklist = normalize_markdown(checklist).lower()
if "authorized human release decision" not in plain_checklist:
    fail("public-beta checklist missing final human release decision control")
if "may not" not in plain_checklist or "final human-decision box" not in plain_checklist:
    fail("public-beta checklist must explicitly prohibit CI from checking the final human decision")

policy = (REVIEW / "RELEASE_POLICY.md").read_text(encoding="utf-8") if (REVIEW / "RELEASE_POLICY.md").exists() else ""
plain_policy = normalize_markdown(policy).lower()
for phrase in ("Public beta", "Superseded", "Only an authorized human release decision", "CI may block release but may not approve it"):
    if normalize_markdown(phrase).lower() not in plain_policy:
        fail(f"release policy missing control: {phrase}")

print(f"HOSI public-beta governance QA: {len(gates)} gates, {len(events)} review events, {len(corrections)} corrections")
if errors:
    for msg in errors:
        print(f"ERROR: {msg}", file=sys.stderr)
    print(f"FAILED: {len(errors)} validation error(s)", file=sys.stderr)
    sys.exit(1)

print("PASS: governance structure is internally consistent")
print("NOTE: PASS does not mean any human gate, peer review, public beta, or release approval has occurred.")