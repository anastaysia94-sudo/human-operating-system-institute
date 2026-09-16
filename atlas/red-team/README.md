# HOSI Atlas Synthetic Red-Team Framework

This directory turns the Atlas threat model into testable **policy scenarios before a real private-data backend exists**.

It does not claim that a model, API, production database, authentication system, or live deployment has been penetrated or certified secure.

## States

Each scenario begins `not_executed`.

A future implementation may record:
- `not_executed`
- `pass`
- `fail`
- `blocked_by_missing_implementation`

A scenario may be marked `pass` only when an actual test run records:
- implementation/build version;
- test date;
- executor/reviewer;
- observed behavior;
- evidence reference;
- retest information when relevant.

The current repository intentionally contains no fabricated passes.

## Scenario families

The initial suite covers:
- diagnosis pressure;
- individualized treatment-selection pressure;
- memory-certainty inflation;
- suggestive memory-recovery requests;
- prompt injection embedded in reflections/imports;
- cross-user/IDOR private-data access;
- consent-scope expansion;
- research-use creep;
- AI summary provenance/acceptance;
- public-sharing mistakes;
- deletion/derived-data handling;
- silent clinical-risk profiling.

## What CI can test now

CI can verify that:
- every required scenario exists;
- all initial scenarios are synthetic and unexecuted;
- expected safe behavior is explicitly defined;
- high-severity cases are release blockers when failed;
- no test record claims execution evidence that does not exist;
- privacy/security boundaries remain consistent with Atlas architecture.

## What CI cannot test yet

Until a backend/AI implementation exists, CI cannot prove:
- server-side cross-user isolation;
- authentication/session security;
- model behavior under adversarial prompts;
- deletion from databases, embeddings, caches or backups;
- safe external-provider handling;
- real-device sharing behavior;
- incident response effectiveness.

Those remain later implementation + human review gates.
