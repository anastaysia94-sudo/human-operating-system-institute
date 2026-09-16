#!/usr/bin/env python3
"""Structural validator for HOSI Atlas synthetic red-team policy scenarios.

This validates scenario coverage and release-blocker semantics before an actual
backend/AI implementation exists. It does not claim any scenario was executed.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "atlas"
SCENARIOS = ATLAS / "red-team" / "scenarios.json"
CONTRACT = ATLAS / "AUTHORIZATION_AND_DATA_BOUNDARY_CONTRACT.md"
REDTEAM_README = ATLAS / "red-team" / "README.md"

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


for path in (CONTRACT, REDTEAM_README, SCENARIOS):
    if not path.exists():
        fail(f"missing required Atlas red-team artifact: {path.relative_to(ROOT)}")

records = load(SCENARIOS)
if not isinstance(records, list):
    fail("scenarios.json must contain an array")
    records = []

required_names = {
    "diagnosis_pressure",
    "individualized_treatment_selection_pressure",
    "memory_certainty_inflation",
    "suggestive_memory_recovery",
    "prompt_injection_inside_reflection",
    "cross_user_idor",
    "consent_scope_expansion",
    "research_use_creep",
    "ai_summary_provenance_overwrite",
    "accidental_public_sharing",
    "deletion_derived_data_gap",
    "silent_clinical_risk_profile",
}

allowed_statuses = {"not_executed","pass","fail","blocked_by_missing_implementation"}
required_fields = {
    "scenario_id","name","category","severity","synthetic_only","status",
    "test_intent","expected_safe_behavior","prohibited_behavior","execution_evidence",
}

ids: set[str] = set()
names: set[str] = set()
for index, record in enumerate(records):
    label = f"scenarios[{index}]"
    if not isinstance(record, dict):
        fail(f"{label} must be an object")
        continue
    missing = sorted(required_fields - set(record))
    if missing:
        fail(f"{label} missing required fields: {', '.join(missing)}")
    scenario_id = record.get("scenario_id")
    name = record.get("name")
    if not isinstance(scenario_id, str) or not re.fullmatch(r"RT-\d{3}", scenario_id):
        fail(f"{label} invalid scenario_id: {scenario_id!r}")
    elif scenario_id in ids:
        fail(f"duplicate scenario_id: {scenario_id}")
    else:
        ids.add(scenario_id)
    if not isinstance(name, str) or not name:
        fail(f"{scenario_id or label} missing name")
    elif name in names:
        fail(f"duplicate scenario name: {name}")
    else:
        names.add(name)
    if record.get("synthetic_only") is not True:
        fail(f"{scenario_id or label} must remain synthetic_only=true in pre-implementation suite")
    if record.get("severity") != "release_blocker_if_failed":
        fail(f"{scenario_id or label} must be a release blocker if failed")
    status = record.get("status")
    if status not in allowed_statuses:
        fail(f"{scenario_id or label} invalid status: {status!r}")
    expected = record.get("expected_safe_behavior")
    prohibited = record.get("prohibited_behavior")
    if not isinstance(expected, list) or not expected:
        fail(f"{scenario_id or label} requires expected_safe_behavior")
    if not isinstance(prohibited, list) or not prohibited:
        fail(f"{scenario_id or label} requires prohibited_behavior")
    evidence = record.get("execution_evidence")
    if status == "not_executed" and evidence is not None:
        fail(f"{scenario_id or label} is not_executed but contains execution evidence")
    if status in {"pass","fail"}:
        if not isinstance(evidence, dict):
            fail(f"{scenario_id or label} status {status} requires structured execution_evidence")
        else:
            for field in ("build_version","test_date","executor","observed_behavior","evidence_ref"):
                if not evidence.get(field):
                    fail(f"{scenario_id or label} executed status requires evidence field {field}")

missing_names = sorted(required_names - names)
if missing_names:
    fail(f"missing required red-team scenarios: {', '.join(missing_names)}")

# This branch has architecture/fixtures, not a live implementation. A synthetic scenario
# may not be magically marked passed before there is execution evidence.
if any(r.get("status") == "pass" for r in records if isinstance(r, dict)):
    fail("pre-implementation Atlas branch must not contain fabricated red-team passes")

contract = CONTRACT.read_text(encoding="utf-8") if CONTRACT.exists() else ""
for phrase in (
    "Server-side authorization",
    "IDs are references, not authorization tokens",
    "Reflection text is untrusted content",
    "Research use requires",
    "Private is the default",
    "AI-generated text is derived data",
    "A UI disappearance alone is not a completed deletion",
):
    if phrase.lower() not in contract.lower():
        fail(f"authorization/data-boundary contract missing safeguard: {phrase}")

readme = REDTEAM_README.read_text(encoding="utf-8") if REDTEAM_README.exists() else ""
if "no fabricated passes" not in readme.lower():
    fail("red-team README must prohibit fabricated pass states")
if "cannot prove" not in readme.lower():
    fail("red-team README must state what CI cannot prove")

print(f"HOSI Atlas red-team QA: {len(records)} synthetic scenarios, 0 fabricated passes expected")
if errors:
    for msg in errors:
        print(f"ERROR: {msg}", file=sys.stderr)
    print(f"FAILED: {len(errors)} validation error(s)", file=sys.stderr)
    sys.exit(1)

print("PASS: synthetic red-team policy coverage is structurally consistent")
print("NOTE: PASS does not mean the scenarios were executed against a production or test implementation.")