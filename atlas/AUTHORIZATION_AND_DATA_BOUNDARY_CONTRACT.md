# HOSI Atlas — Authorization & Data Boundary Contract

This contract defines non-negotiable behavior for any future Atlas backend. It is architecture, not evidence that a production implementation exists.

## 1. Ownership boundary

Every Atlas object must resolve to exactly one owning author/account context unless it is an explicitly derived/export/public object with separate provenance.

Objects include:
- Atlas root
- reflection/oral-history entries
- consent records
- AI summaries
- knowledge-graph edges
- provenance events
- exports
- deletion requests
- sharing grants

## 2. Server-side authorization

Authorization must be enforced server-side on every private read/write operation.

Never rely only on:
- hidden UI controls
- unguessable-looking IDs
- client-side route guards
- JavaScript checks
- prompt instructions to the AI

For every object access:
1. authenticate the requester where authentication is required;
2. resolve the object;
3. resolve its owner and active sharing grants;
4. evaluate the requested action against server-side policy;
5. deny by default when authorization is absent or ambiguous;
6. log the security-relevant event without logging unnecessary narrative content.

## 3. Cross-user isolation

A user must not be able to read, infer, search, export, mutate, summarize or link another author's private Atlas data merely by changing:
- object ID
- URL
- query parameter
- API body
- graph node identifier
- export identifier
- AI prompt

IDs are references, not authorization tokens.

## 4. AI boundary

The AI service receives only the minimum Atlas objects authorized for the current purpose.

Do not provide the model with:
- another user's private records;
- a whole Atlas when consent covers selected entries only;
- research datasets when consent is only for educational summarization;
- hidden diagnostic/risk labels created from ordinary reflections.

Reflection text is untrusted content. Instructions embedded inside a reflection/import must never override platform policy, system instructions, authorization, consent, or data-scope controls.

## 5. Consent boundary

Consent is purpose-specific.

Separate purposes include:
- storage
- AI summarization
- AI theme extraction
- sharing with a named person/group
- public display
- analytics
- research use

Granting one purpose does not imply another.

Revocation must stop future processing for the revoked purpose and trigger the disclosed handling of derived data.

## 6. Public sharing

Private is the default.

Before changing an object to public:
- identify exactly which object(s) will become public;
- show the current content or a clear preview;
- distinguish public web publication from private/named sharing;
- require an explicit confirmation action;
- create provenance;
- provide an unshare path.

One accidental click or ambiguous toggle must not silently publish an entire Atlas.

## 7. AI output boundary

AI-generated text is derived data and must remain distinguishable from author-authored text.

An AI summary may not become accepted author narrative until the author explicitly reviews/accepts it. Rejected or superseded AI output remains traceable according to retention policy and must not silently reappear as author testimony.

## 8. Memory and corroboration boundary

The system must preserve separate concepts for:
- author memory confidence;
- corroborating evidence status;
- alternative interpretations;
- AI-generated interpretation.

Neither AI confidence nor author confidence converts an autobiographical memory into verified fact.

## 9. Research boundary

Student/founder Atlas data must never silently become institutional research data.

Research use requires:
- separate consent;
- defined research purpose;
- defined data scope;
- withdrawal/retention rules;
- required ethical/institutional review where applicable.

## 10. Logs and telemetry

Avoid raw narrative content in ordinary application/security telemetry.

Prefer:
- object IDs
- event types
- authorization result
- timestamps
- non-sensitive error codes

Sensitive payload logging must be exceptional, justified, access-controlled, time-limited and disclosed where required.

## 11. Export

Export authorization must be evaluated like any other private read.

Exports must:
- include only the requesting author's authorized scope;
- not include hidden records belonging to other users;
- label AI-generated/derived content;
- include provenance where appropriate;
- be protected from predictable/unauthorized download URLs.

## 12. Delete

Deletion design must account for:
- primary records
- derived summaries/themes/embeddings
- graph edges
- search indexes
- cached copies
- exports retained by HOSI
- backups according to a disclosed retention window
- audit/security records that legitimately must remain

A UI disappearance alone is not a completed deletion.

## 13. Launch blockers

Any of the following is a private-data pilot/public-beta blocker:
- reproducible cross-user private-data access;
- client-only authorization for private objects;
- AI processing outside active consent scope;
- public sharing without explicit confirmation;
- research use without separate consent;
- AI-generated narrative silently becoming author-authored narrative;
- covert diagnosis/risk profiling from ordinary educational reflections;
- inability to identify or contain private-data exposure.

Human privacy/security review and implementation testing are still required before real sensitive data is collected.