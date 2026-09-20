# HOSI Atlas MVP — Prototype Plan

## Objective

Produce a privacy-first Atlas prototype that demonstrates author control, provenance, consent, AI-review states, export/delete flows, and cross-user isolation **before** any real sensitive learner data is collected.

## Phase 0 — Architecture only

Status represented by this branch.

Deliverables:
- schemas
- privacy rules
- threat model
- UX flows
- validator
- synthetic fixtures only

Gate:
- no sensitive production data
- no production claims

## Phase 1 — Local synthetic prototype

Use only synthetic personas and fictional reflections.

Implement:
- create Atlas
- create/edit/delete reflection
- privacy state
- memory-confidence vs fact-status fields
- consent records
- AI-summary state machine using mocked output first
- provenance log
- export JSON
- delete simulation

Tests:
- schema validation
- state transitions
- permission defaults
- rejected AI summary cannot become accepted narrative

## Phase 2 — Authenticated test environment with synthetic accounts

Add:
- authentication
- server-side authorization
- isolated user records
- server-side consent enforcement
- short-lived export links
- derived-data deletion orchestration
- audit logs without narrative content

Required adversarial tests:
- IDOR/cross-user reads
- cross-user writes
- export contamination
- search/vector leakage
- session theft/revocation scenarios
- support/admin access controls

Gate:
- zero known cross-user isolation failures

## Phase 3 — AI retrieval prototype with synthetic/private test data only

Add:
- scoped retrieval
- purpose-specific consent checks
- source-entry citations in AI summaries
- uncertainty notes
- pending user approval for inferred themes/graph edges
- prompt-injection defenses

Red team:
- diagnosis requests
- requests to reveal another user
- malicious instructions embedded in reflections
- pressure to treat memory confidence as truth
- attempts to bypass withdrawn consent

Gate:
- AI cannot directly query unrestricted user data
- authorization remains outside the model
- prohibited inference tests pass at agreed threshold and failures are documented

## Phase 4 — Accessibility & privacy usability test

Test with synthetic content and representative users/reviewers.

Evaluate:
- whether users understand private vs public
- whether AI status is obvious
- whether consent withdrawal is understandable
- whether delete/export is findable
- screen-reader/keyboard/mobile usability
- cognitive load of prompts and controls

Gate:
- blocking accessibility/privacy usability issues resolved

## Phase 5 — Limited real-user pilot decision

Before any real sensitive pilot:
- privacy policy approved
- terms/consent reviewed for target jurisdiction/population
- incident response approved
- backup and deletion behavior tested
- security review completed
- human review of non-diagnostic AI guardrails
- data-retention schedule approved
- pilot protocol defines exactly what data is collected and why

Default pilot should request the least sensitive data possible.

## Phase 6 — Pilot

Pilot with explicit informed participants only.

Collect:
- usability findings
- privacy comprehension
- false/inaccurate AI summaries
- consent failures
- deletion/export failures
- accessibility issues
- unexpected sensitive inference
- user correction rates

Do not silently turn pilot reflections into research data.

## Phase 7 — Release decision

Release requires evidence that:
- privacy controls work
- authorization isolation works
- export works
- deletion works according to documented policy
- AI provenance works
- user review/correction works
- incident response exists
- accessibility gates pass
- known risks are documented

## Suggested technical implementation

This document intentionally avoids locking HOSI into a vendor before requirements are validated.

Recommended architecture characteristics:
- relational database with explicit author/tenant ownership fields
- server-side authorization for every record
- encrypted transport
- encrypted secret management
- separate narrative data from telemetry
- background job/state machine for export/deletion
- append-oriented provenance events with careful deletion/privacy design
- vector/search indexes scoped by author/tenant
- AI gateway that receives only consent-authorized records

## Data-model entities

MVP entities:
- Atlas
- ReflectionEntry
- ConsentRecord
- AISummary
- ProvenanceEvent
- KnowledgeGraphEdge
- ExportJob
- DeletionJob

Future entities only after requirement review:
- SharedCollection
- TeacherFeedback
- ResearchConsent
- ResearchDatasetMembership
- CertificatePortfolioLink

## Definition of prototype-complete

Prototype-complete does **not** mean production-ready.

The prototype milestone is complete when:
- schemas validate
- synthetic state transitions work
- private-default behavior is demonstrated
- consent gates work
- AI summary review states work
- provenance works
- export/delete simulations work
- threat-model tests are runnable/documented
- no real sensitive data was needed to prove the architecture

## Definition of production-ready

Production-ready requires real security/privacy/accessibility verification, not a document saying “secure.”

HOSI should treat “we wrote the threat model” the same way aerospace treats “we drew the parachute”: encouraging, but rather premature to jump.
