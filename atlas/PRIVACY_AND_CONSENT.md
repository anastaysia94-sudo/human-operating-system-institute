# HOSI Atlas MVP — Privacy, Consent, Export & Deletion Rules

## 1. Ownership

The Atlas belongs to its author. HOSI provides storage, organization, educational linking, and approved AI assistance as a steward.

No terms, UI text, or implementation should imply that HOSI owns the author's life narrative.

## 2. Private by default

New Atlases and new entries default to `private`.

Public display, selected-person sharing, institutional access, AI processing, analytics, and research use require separate affirmative controls where applicable.

Silence is not consent. Continuing to use the learning platform is not consent to process optional sensitive Atlas material.

## 3. Data minimization

Do not collect information merely because it might someday be useful.

For every field or event, ask:
1. What user-requested function needs it?
2. Can that function work with less-sensitive data?
3. Can the value be computed locally/temporarily instead of stored?
4. When can it be deleted?

## 4. Sensitive information is optional

General HOSI education must not require disclosure of:
- diagnoses
- trauma history
- brain injury history
- medication or treatment history
- faith
- sexuality or intimate relationships
- family conflict
- legal history
- financial information
- other highly sensitive personal material

A user may voluntarily record such information in a private Atlas. The platform should remind them that they can skip, redact, generalize, or delete it.

## 5. Granular consent

Consent must be purpose-specific. Store separate records for at least:
- Atlas storage
- AI summarization
- personalization
- sharing
- public display
- analytics
- research use

Research use is never implied by educational use.

Withdrawing one purpose must not unnecessarily disable unrelated educational functions.

## 6. AI processing

Before AI processes private entries, the product must show:
- what entries/categories will be processed
- the purpose
- that output is AI-generated
- that the user can review/reject it
- whether the output will be stored
- how to withdraw permission

AI-generated summaries remain unaccepted until explicit author approval.

AI must use uncertainty language for inferred themes and must not infer or assign diagnoses, clinical risk labels, personality disorders, intelligence, or identity certainty from ordinary reflections.

## 7. Memory and factual status

`memory_confidence` is subjective confidence only.

It must not be displayed or used as a probability that an event occurred.

Corroboration, conflicting evidence, fact status, and alternative interpretations remain separate fields.

## 8. Sharing

Sharing should be object-scoped and revocable where technically possible.

The UI must distinguish:
- private
- selected people
- institutional private
- public

Before making sensitive content public, require a deliberate confirmation screen that identifies what will become public.

Do not default to public links for private Atlas content.

## 9. Export

The author must be able to request a machine-readable export that includes, where applicable:
- Atlas metadata
- entries
- consent records
- accepted/rejected AI summaries
- provenance history
- tags and relationships
- privacy settings

Export should not silently omit provenance or rejected AI content if that content remains stored and belongs to the author's account data.

Export packages must not contain other users' information.

## 10. Correction

Edits must preserve provenance sufficient to distinguish:
- original author text
- later author edits
- AI-generated text
- accepted AI text
- editor/authorized-human changes

A user should be able to correct an inaccurate AI summary without rewriting the original reflection.

## 11. Deletion

Deletion controls must be understandable and accessible.

The product must distinguish:
- deleting one entry
- deleting one AI summary
- clearing a category
- deleting the entire Atlas
- deleting an account, if account deletion is broader than Atlas deletion

When deletion is requested:
1. record a deletion provenance event without unnecessarily preserving deleted content;
2. remove active copies according to the documented deletion process;
3. handle backups according to a documented expiry process;
4. report any legally/technically required exception honestly;
5. do not claim instantaneous erasure from systems where it did not occur.

The MVP must define this process before collecting real sensitive data.

## 12. Retention

Default rule: retain author-created Atlas data while the Atlas remains active and the author wants it stored.

Derived AI data should not outlive the source/purpose without a documented reason and consent basis.

Telemetry should be minimized and separated from private narrative content.

## 13. Research boundary

No private Atlas content becomes an HOSI research dataset merely because it exists on the platform.

Future research use requires:
- a separate consent purpose
- understandable description of use
- appropriate ethics/governance review
- data-minimization/de-identification plan where applicable
- withdrawal rules
- security controls

## 14. Children and legally protected populations

The MVP does not assume it is ready for child accounts or other legally protected populations.

Before enabling those populations, HOSI must perform jurisdiction-appropriate legal/privacy review and implement age/guardian/consent controls where required.

## 15. Security boundary

Never place real Atlas content, credentials, encryption keys, access tokens, or private user exports in the public GitHub repository.

Production launch requires verified authentication, authorization, encryption where appropriate, audit logging, incident response, secure backup/recovery, deletion testing, cross-user isolation testing, and red-team exercises.

## 16. No dark patterns

Do not make privacy-protective choices harder than disclosure choices.

Do not:
- pre-check sensitive sharing
- hide deletion
- repeatedly nag for trauma/diagnosis disclosure
- make AI processing a condition of basic education
- frame refusal to disclose as incomplete participation

Privacy is a product requirement, not the tiny gray sentence beneath the exciting button.
