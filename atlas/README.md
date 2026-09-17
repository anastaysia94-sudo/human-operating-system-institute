# HOSI Atlas MVP

The HOSI Atlas is a learner-controlled reflective and educational archive derived from the Founder's Atlas concept.

## Core rule

**The Atlas belongs to its author. HOSI is its steward, not its owner.**

The MVP is designed before collecting sensitive information. The repository contains schemas, privacy rules, threat modeling, UX flows, and synthetic examples only. It must not contain real private learner narratives, diagnoses, treatment histories, credentials, or secrets.

## Atlas types

- `founder` — autobiographical/oral-history and institutional-history use.
- `learner` — private learning/reflection archive for students or patrons.
- `visitor` — optional lightweight public/guest educational profile with minimal storage.

Atlas type does not change the author's ownership rights.

## Core capabilities

- timeline entries
- reflections
- goals
- values and beliefs when voluntarily supplied
- projects and achievements
- learning history
- links to HOSI lessons/research records
- knowledge-graph relationships
- user-approved AI summaries
- correction history
- export
- deletion requests/state
- privacy controls
- provenance

## Non-capabilities

Atlas AI must not:

- diagnose
- prescribe
- make medication changes
- impersonate a clinician
- silently infer psychiatric/neurological conditions
- assign identity labels with certainty
- make treatment decisions
- secretly turn personal reflections into institutional research data
- claim that memory confidence proves factual accuracy

## Sensitive data principle

Sensitive fields are optional. A learner should be able to use the educational platform without disclosing diagnosis, trauma, treatment, faith, intimate relationships, health history, or other highly personal information.

## AI summary lifecycle

An AI-generated summary is not part of the author's accepted narrative until the author explicitly accepts it.

States:

1. `generated`
2. `user_review_required`
3. `accepted`
4. `rejected`
5. `superseded`

Rejected summaries remain outside the accepted Atlas narrative and should be deletable under the applicable retention policy.

## Memory confidence

Memory confidence records how confident the author feels about a recollection. It is **not** a factual-accuracy score.

Corroboration, conflicting evidence, uncertainty, and alternative interpretations are tracked separately.

## Files

- `schemas/atlas.schema.json` — top-level Atlas/account-independent data envelope.
- `schemas/reflection-entry.schema.json` — reflection/oral-history entry model.
- `schemas/consent-record.schema.json` — granular consent model.
- `schemas/ai-summary.schema.json` — reviewable AI-summary model.
- `schemas/provenance-event.schema.json` — immutable-style provenance event model.
- `PRIVACY_AND_CONSENT.md` — consent, minimization, export, deletion, and retention rules.
- `THREAT_MODEL.md` — privacy/security abuse cases and mitigations.
- `UX_FLOW.md` — user-control-first screens and flows.
- `PROTOTYPE_PLAN.md` — implementation sequence before real sensitive data collection.

## Release boundary

This MVP is architecture and policy scaffolding. It is not a deployed production service and must not be represented as one until authentication, authorization, encryption, deletion/export, audit logging, backup/recovery, privacy testing, and red-team gates actually pass.
