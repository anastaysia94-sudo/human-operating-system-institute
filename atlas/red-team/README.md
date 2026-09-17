# HOSI Atlas Synthetic Red-Team Framework

This directory turns the Atlas threat model into testable policy scenarios. The branch now includes a small **synthetic executable backend**, so backend/data-boundary scenarios can move from paper to actual tests while AI-model and public-sharing scenarios remain blocked until those components exist.

It does not claim that a production database, production API, production model, real device, or live deployment has been penetrated or certified secure.

## States

A scenario may be:
- `not_executed`
- `pass`
- `fail`
- `blocked_by_missing_implementation`

A scenario may be marked `pass` only when an actual test run records:
- implementation/build version;
- test date;
- executor/reviewer;
- observed behavior;
- evidence reference.

**No fabricated passes.** A green synthetic test is evidence only for the specific implementation and behavior it exercised.

## What is executable now

The Python/SQLite synthetic backend now exercises:
- reflection text remaining untrusted data rather than instructions;
- server-side cross-user/IDOR isolation;
- owner-scoped search and export;
- selected-entry AI-summary consent without whole-Atlas consent expansion;
- separate research consent;
- AI summaries staying in `user_review_required` state;
- deletion cascading through live primary/derived records and stored export snapshots;
- session revocation and account deletion;
- audit logs that retain object/security metadata without copying ordinary narrative bodies.

These tests use only fictional `.invalid` accounts and an in-memory database.

## What remains blocked

The current repository still lacks a real Atlas AI model pipeline and a public-sharing implementation. Therefore these scenarios cannot honestly pass yet:
- diagnosis pressure;
- individualized treatment selection;
- memory-certainty inflation;
- suggestive memory recovery;
- accidental public sharing;
- silent clinical-risk profiling.

## What CI can prove

CI can prove that the current synthetic backend behaved as asserted in deterministic tests and that the recorded scenario evidence matches the expected pass/blocker set.

## What CI cannot prove

CI **cannot prove**:
- production security or regulatory compliance;
- independent penetration-test results;
- production encryption/key-management quality;
- safe behavior from a future external AI model under adversarial prompts;
- deletion from future backups/embeddings/caches that do not exist yet;
- real-device sharing behavior;
- incident-response effectiveness under a real breach;
- accessibility, privacy, clinical, or legal approval by qualified humans.

Those remain implementation and human-review gates before real sensitive Atlas data may be collected.
