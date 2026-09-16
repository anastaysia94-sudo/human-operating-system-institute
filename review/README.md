# HOSI Review, QA & Public Beta Framework

This directory defines the gates required before HOSI material may move from draft/prototype status toward reviewed publication or public beta.

## Core rule

**Generation is not review. Automation is not human approval. A green CI run is not peer review, clinical review, accessibility certification, learner validation, accreditation, or release authorization.**

HOSI uses explicit review records so that future agents, editors, and developers cannot silently upgrade status merely because content exists.

## Required gate families

1. Subject-matter review
2. Citation / claim-to-source audit
3. Medical / safety review where applicable
4. Lived-experience review where applicable
5. Accessibility review
6. Assessment / rubric review where applicable
7. Privacy / security review where applicable
8. Atlas / AI red-team where applicable
9. Learner pilot for public-beta readiness
10. Correction-resolution pass
11. Final automated QA
12. Explicit human release decision

Not every artifact requires every specialty gate. The release manifest must identify which gates apply and why.

## Human-only states

The following states must never be set solely by an AI agent or CI workflow:

- `human_reviewed`
- `peer_review_complete`
- `clinical_safety_approved`
- `accessibility_approved`
- `pilot_approved`
- `release_approved`
- `final`

AI may prepare packets, discover sources, flag inconsistencies, run deterministic checks, and summarize reviewer feedback. It may not impersonate the reviewer whose expertise is required by a gate.

## Review evidence

A completed human gate requires a review-event record containing:

- unique review ID
- artifact or scope reviewed
- immutable source/version reference
- reviewer role
- reviewer identity or controlled pseudonymous reviewer ID
- date
- decision
- blocking findings
- non-blocking findings
- correction requirements
- conflict-of-interest statement
- re-review requirement

## Release principle

No course, research claim set, Atlas system, public campus, credential workflow, or public beta should be labeled final merely because its architecture is complete.

The release checklist must remain visibly incomplete until actual review evidence exists.