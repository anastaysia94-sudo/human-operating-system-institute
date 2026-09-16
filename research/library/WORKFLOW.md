# HOSI Research Library — Verification & Correction Workflow

## Principle

A source is not a claim. A claim is not a conclusion about an individual. A green CI check is not peer review.

HOSI therefore separates source discovery, claim extraction, evidence appraisal, human review, curriculum approval, and publication.

## Required sequence

### 1. RESEARCH QUESTION
Write the question before searching.

Record:
- domain
- target population
- intervention/exposure when relevant
- comparator when relevant
- outcome
- intended curriculum use

### 2. DISCOVER
Prefer current authoritative guidelines, systematic reviews/meta-analyses, high-quality trials, and primary research appropriate to the question.

Discovery may be AI-assisted. Discovery alone does not change a source to `metadata_verified`.

### 3. VERIFY SOURCE METADATA
Check the source against the publisher, journal, PubMed/NCBI, government authority, or equivalent authoritative record.

Verify where applicable:
- exact title
- authors/issuing body
- publication year
- DOI
- canonical URL
- source type
- update/revision date
- retraction/withdrawal/supersession status

Only after this step may the source become `metadata_verified`.

### 4. READ THE RELEVANT FULL TEXT
Before curriculum publication, a qualified reviewer must inspect enough of the full source to verify the intended claim.

Extract:
- population
- design
- intervention/exposure
- comparator
- outcome
- effect estimate when relevant
- uncertainty
- risk of bias
- limitations
- applicability
- conflicts/funding when relevant

A source may become `full_text_checked` only when this work actually occurred.

### 5. CREATE THE CLAIM RECORD
Write one bounded claim per evidence card whenever practical.

Avoid compound claims such as:
> Therapy X changes mechanism Y, treats diagnosis Z, and works for everyone.

Split claims so that each can be independently supported, contradicted, revised, or held.

### 6. SEARCH FOR CONTRADICTORY / SUPERSEDING EVIDENCE
Search specifically for:
- newer guidelines
- newer systematic reviews/meta-analyses
- failed replications
- conflicting trials
- population-specific exceptions
- evidence that limits generalization
- retractions, expressions of concern, withdrawals, or guideline replacement

Set the contradiction field honestly:
- `not_searched`
- `searched_none_material_found`
- `material_conflict_found`
- `mixed_evidence`

`searched_none_material_found` never means contradictory evidence cannot exist.

### 7. RATE THE CLAIM
Assign HOSI A–E confidence to the **claim**, not the paper.

- **A — High confidence:** consistent, directly applicable, high-quality evidence.
- **B — Moderate confidence:** useful evidence with meaningful limitations or indirectness.
- **C — Limited/mixed:** sparse, heterogeneous, indirect, or conflicting evidence.
- **D — Emerging/preliminary:** early evidence requiring substantial confirmation.
- **E — Insufficient:** not enough reliable evidence for a confident educational claim.

Record why the rating was chosen.

### 8. HUMAN REVIEW
A real reviewer records a review event with:
- reviewer identity
- role/expertise
- conflict-of-interest disclosure
- date
- source/claim IDs reviewed
- decision
- requested corrections
- repository commit reviewed

AI output may prepare the packet but must not impersonate this event.

### 9. APPROVE FOR CURRICULUM
`approved_for_curriculum` is allowed only when:
- source matching is complete enough for the claim
- contradiction search is complete enough for the claim
- applicable human review is recorded
- blocking corrections are resolved
- safety/scope requirements are satisfied

Approval means the claim may be used in curriculum within its stated bounds. It does not create medical advice, accreditation, or universal truth.

### 10. PUBLISH / RELEASE
Publication occurs through the curriculum/platform release process, not this research library alone.

A merged evidence card is not automatically public curriculum.

### 11. MONITOR / CORRECT
Re-check high-impact and rapidly changing claims on a defined cadence.

Trigger immediate review when:
- a guideline is replaced
- a source is retracted or corrected
- a major contradictory review appears
- a safety signal changes
- a curriculum claim is challenged with credible evidence

Corrections must preserve visible revision history.

## AI permissions

AI may:
- discover candidate sources
- verify public metadata
- draft bounded claim cards
- summarize abstracts/full text that it can access
- identify possible contradictions
- propose evidence ratings
- run validation
- prepare reviewer packets

AI may **not** truthfully mark a record `human_reviewed` or `approved_for_curriculum` without a corresponding real human review event.

## Lived experience

Lived experience is legitimate knowledge for questions it can answer, including usability, dignity, stigma, acceptability, meaning, and real-world burden.

It is not automatically evidence of:
- population prevalence
- causal mechanism
- treatment efficacy
- diagnostic validity

The reverse is also true: population research does not erase an individual's experience.

## Medication boundary

HOSI may teach pharmacology and comparative evidence. It must not use a library record to instruct a learner to start, stop, or alter medication.

## Correction format

Each correction should record:
- affected source/claim ID
- previous text/status/rating
- corrected text/status/rating
- reason
- supporting source(s)
- reviewer/editor
- date
- repository commit

The goal is not to appear infallible. The goal is to be correctable without becoming epistemic soup.
