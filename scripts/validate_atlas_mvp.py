#!/usr/bin/env python3
"""Deterministic structural/privacy validator for the HOSI Atlas MVP.

This validator checks schemas, the synthetic fixture, provenance links, consent
coverage, privacy defaults, and AI review-state invariants. It does not prove
production security, privacy-law compliance, clinical safety, or human review.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "atlas"
SCHEMAS = ATLAS / "schemas"
FIXTURE = ATLAS / "fixtures" / "synthetic-atlas-bundle.json"

REQUIRED_DOCS = [
    ATLAS / "README.md",
    ATLAS / "PRIVACY_AND_CONSENT.md",
    ATLAS / "THREAT_MODEL.md",
    ATLAS / "UX_FLOW.md",
    ATLAS / "PROTOTYPE_PLAN.md",
]

REQUIRED_SCHEMAS = [
    SCHEMAS / "atlas.schema.json",
    SCHEMAS / "reflection-entry.schema.json",
    SCHEMAS / "consent-record.schema.json",
    SCHEMAS / "ai-summary.schema.json",
    SCHEMAS / "provenance-event.schema.json",
    SCHEMAS / "knowledge-graph-edge.schema.json",
]

errors: list[str] = []
warnings: list[str] = []


def error(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        error(f"missing file: {path.relative_to(ROOT)}")
        return None
    except json.JSONDecodeError as exc:
        error(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return None


for doc in REQUIRED_DOCS:
    if not doc.exists():
        error(f"missing required Atlas document: {doc.relative_to(ROOT)}")

for schema_path in REQUIRED_SCHEMAS:
    schema = load_json(schema_path)
    if schema is not None and not isinstance(schema, dict):
        error(f"schema must be a JSON object: {schema_path.relative_to(ROOT)}")

bundle = load_json(FIXTURE)
if not isinstance(bundle, dict):
    error("synthetic fixture must be a JSON object")
    bundle = {}

notice = bundle.get("fixture_notice", "")
if "Synthetic" not in notice and "synthetic" not in notice:
    error("fixture_notice must explicitly identify fixture data as synthetic")

atlas = bundle.get("atlas")
entries = bundle.get("entries", [])
consents = bundle.get("consents", [])
summaries = bundle.get("ai_summaries", [])
edges = bundle.get("edges", [])
provenance = bundle.get("provenance_events", [])

if not isinstance(atlas, dict):
    error("fixture atlas must be an object")
    atlas = {}
for name, value in {
    "entries": entries,
    "consents": consents,
    "ai_summaries": summaries,
    "edges": edges,
    "provenance_events": provenance,
}.items():
    if not isinstance(value, list):
        error(f"fixture {name} must be an array")

atlas_id = atlas.get("atlas_id")
if atlas.get("ownership") != "author_owned_hosi_stewarded":
    error("Atlas ownership must remain author_owned_hosi_stewarded")
if atlas.get("privacy_default") != "private":
    error("Atlas privacy_default must be private")
if not str(atlas.get("author_id", "")).startswith("synthetic-"):
    error("QA fixture author_id must clearly be synthetic")

entry_by_id = {e.get("entry_id"): e for e in entries if isinstance(e, dict)}
consent_by_id = {c.get("consent_id"): c for c in consents if isinstance(c, dict)}
summary_by_id = {s.get("ai_summary_id"): s for s in summaries if isinstance(s, dict)}
edge_by_id = {e.get("edge_id"): e for e in edges if isinstance(e, dict)}
prov_by_id = {p.get("provenance_event_id"): p for p in provenance if isinstance(p, dict)}

for label, mapping in {
    "entry": entry_by_id,
    "consent": consent_by_id,
    "AI summary": summary_by_id,
    "edge": edge_by_id,
    "provenance event": prov_by_id,
}.items():
    if None in mapping:
        error(f"{label} record missing ID")
    if len(mapping) != len([x for x in {
        "entry": entries,
        "consent": consents,
        "AI summary": summaries,
        "edge": edges,
        "provenance event": provenance,
    }[label] if isinstance(x, dict)]):
        error(f"duplicate or missing IDs detected in {label} records")

# Top-level references must resolve.
for eid in atlas.get("entry_ids", []):
    if eid not in entry_by_id:
        error(f"Atlas references unknown entry {eid}")
for cid in atlas.get("consent_record_ids", []):
    if cid not in consent_by_id:
        error(f"Atlas references unknown consent {cid}")
for sid in atlas.get("ai_summary_ids", []):
    if sid not in summary_by_id:
        error(f"Atlas references unknown AI summary {sid}")
for edge_id in atlas.get("knowledge_graph_edge_ids", []):
    if edge_id not in edge_by_id:
        error(f"Atlas references unknown graph edge {edge_id}")
for pid in atlas.get("provenance_event_ids", []):
    if pid not in prov_by_id:
        error(f"Atlas references unknown provenance event {pid}")

# Entry privacy and provenance invariants.
for eid, entry in entry_by_id.items():
    if entry.get("atlas_id") != atlas_id:
        error(f"{eid} belongs to a different atlas")
    controls = entry.get("author_control", {})
    if not isinstance(controls, dict):
        error(f"{eid} author_control must be an object")
        continue
    if controls.get("visibility") == "public" and not controls.get("sharing_allowed"):
        error(f"{eid} cannot be public while sharing_allowed is false")
    if controls.get("research_use_allowed") and entry.get("sensitivity") == "highly_sensitive":
        warn(f"{eid}: highly sensitive fixture data marked for research use; human governance review would be required")
    for pid in entry.get("provenance_event_ids", []):
        if pid not in prov_by_id:
            error(f"{eid} references unknown provenance event {pid}")

# Consent invariants.
for cid, consent in consent_by_id.items():
    if consent.get("atlas_id") != atlas_id:
        error(f"{cid} belongs to a different atlas")
    pid = consent.get("provenance_event_id")
    if pid not in prov_by_id:
        error(f"{cid} references unknown provenance event {pid}")
    scope = consent.get("scope", {})
    if isinstance(scope, dict):
        for eid in scope.get("entry_ids", []):
            if eid not in entry_by_id:
                error(f"{cid} scopes unknown entry {eid}")

# AI summaries require active purpose-matched consent and author review before acceptance.
for sid, summary in summary_by_id.items():
    if summary.get("atlas_id") != atlas_id:
        error(f"{sid} belongs to a different atlas")
    consent_id = summary.get("consent_record_id")
    consent = consent_by_id.get(consent_id)
    if not consent:
        error(f"{sid} references missing consent {consent_id}")
    else:
        if consent.get("purpose") != "ai_summary":
            error(f"{sid} consent {consent_id} is not for ai_summary")
        if consent.get("status") != "granted":
            error(f"{sid} consent {consent_id} is not granted")
        scope = consent.get("scope", {})
        if isinstance(scope, dict) and not scope.get("all_entries", False):
            allowed = set(scope.get("entry_ids", []))
            for eid in summary.get("source_entry_ids", []):
                if eid not in allowed:
                    error(f"{sid} processes {eid} outside consent scope")
    for eid in summary.get("source_entry_ids", []):
        if eid not in entry_by_id:
            error(f"{sid} references unknown source entry {eid}")
    status = summary.get("status")
    if status == "accepted":
        if summary.get("reviewed_by_author") is not True:
            error(f"{sid} accepted without reviewed_by_author=true")
        if not summary.get("reviewed_at"):
            error(f"{sid} accepted without reviewed_at timestamp")
    if status in {"generated", "user_review_required"} and summary.get("reviewed_by_author") is True:
        warn(f"{sid}: review flag is true while status is still {status}")
    if summary.get("model_disclosure", {}).get("ai_generated") is not True:
        error(f"{sid} must disclose that it is AI generated")
    if not summary.get("uncertainty_note"):
        error(f"{sid} requires an uncertainty note")
    for pid in summary.get("provenance_event_ids", []):
        if pid not in prov_by_id:
            error(f"{sid} references unknown provenance event {pid}")

# AI-suggested graph edges cannot silently become active.
for edge_id, edge in edge_by_id.items():
    if edge.get("atlas_id") != atlas_id:
        error(f"{edge_id} belongs to a different atlas")
    if edge.get("provenance_type") == "ai_suggested" and edge.get("status") == "active" and not edge.get("reviewed_at"):
        error(f"{edge_id} is an active AI-suggested edge without author review timestamp")
    if edge.get("provenance_type") == "ai_suggested" and not edge.get("uncertainty_note"):
        error(f"{edge_id} AI suggestion lacks uncertainty note")
    if edge.get("provenance_event_id") not in prov_by_id:
        error(f"{edge_id} references unknown provenance event")

# Provenance objects must stay within the Atlas and never pretend AI is the author.
for pid, event in prov_by_id.items():
    if event.get("atlas_id") != atlas_id:
        error(f"{pid} belongs to a different atlas")
    if event.get("actor_type") == "ai_system" and event.get("event_type") in {"created", "edited"}:
        warn(f"{pid}: AI directly created/edited an Atlas object; ensure output is clearly derived and user-reviewable")

# Fixture must not simulate research consent as granted; the MVP proves educational privacy first.
for cid, consent in consent_by_id.items():
    if consent.get("purpose") == "research_use" and consent.get("status") == "granted":
        error(f"{cid}: synthetic MVP fixture must not pre-enable research_use consent")

# The fixture must demonstrate an unaccepted AI summary, not a magically pre-approved one.
if summaries and not any(s.get("status") == "user_review_required" for s in summaries if isinstance(s, dict)):
    error("synthetic fixture must demonstrate at least one AI summary awaiting user review")

print(
    f"HOSI Atlas QA: {len(entries)} entries, {len(consents)} consents, "
    f"{len(summaries)} AI summaries, {len(edges)} edges, {len(provenance)} provenance events"
)
for message in warnings:
    print(f"WARNING: {message}")

if errors:
    for message in errors:
        print(f"ERROR: {message}", file=sys.stderr)
    print(f"FAILED: {len(errors)} validation error(s)", file=sys.stderr)
    sys.exit(1)

print("PASS: Atlas structural/privacy-state validation succeeded")
print("NOTE: PASS does not prove production security, privacy compliance, clinical safety, or human review.")
