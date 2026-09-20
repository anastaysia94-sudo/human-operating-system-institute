# HOSI Atlas incident response — implementation draft

Status: **required operating procedure for any private-data pilot; human privacy/security review required before production.**

## Purpose

If Atlas private data may have been exposed, altered, improperly shared, or processed outside consent, the first job is containment and evidence preservation, not public-relations improvisation.

## Severity triggers

Treat these as high-severity until investigated:

- one user can access another user's private Atlas object;
- a private object becomes public without explicit confirmation;
- AI processing receives data outside active consent scope;
- research use occurs without separate research consent;
- logs or telemetry contain raw private narrative unexpectedly;
- deleted live data remains active in derived systems;
- session/token/key compromise is suspected;
- covert clinical or diagnostic profiling is discovered.

## Response sequence

1. **Contain:** disable the affected route, feature, sharing path, model job, token, or integration.
2. **Preserve minimal evidence:** retain security metadata needed to understand the incident without copying unnecessary narrative content.
3. **Scope:** identify affected users, objects, time window, derived systems, exports, backups, and consent purposes.
4. **Eradicate:** fix the authorization, consent, sharing, logging, or lifecycle defect.
5. **Recover:** restore service gradually using synthetic tests and targeted verification first.
6. **Notify:** follow applicable legal/contractual/user-notification requirements after human review; do not invent universal notification deadlines in this engineering document.
7. **Correct:** remove unauthorized derived data and rotate/revoke credentials where appropriate.
8. **Learn:** write a blameless post-incident record with root cause, impact, corrective actions, and regression tests.

## Required technical evidence before private-data pilot

- reproducible cross-user isolation tests;
- session invalidation tests;
- deletion/derived-data tests;
- consent-scope tests;
- audit logs that exclude ordinary narrative bodies;
- restore/deletion retention tests once backups exist;
- a named human escalation path and on-call/contact procedure.

The repository now implements the first five items against synthetic data. Production operations and named human escalation remain release gates.
