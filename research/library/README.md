# HOSI Research Library MVP

This directory is the machine-readable evidence layer for the Human Operating System Institute.

It does **not** turn a citation into a verified claim merely because a URL resolves. HOSI keeps four distinct evidence objects:

1. **Source record** — what the publication/guideline/resource is.
2. **Claim record** — the exact educational or clinical claim HOSI wants to make.
3. **Contradiction / supersession search record** — what current evidence was searched for a bounded claim, what sources were checked, and whether material conflict or qualifying evidence was found.
4. **Review event** — who actually checked the source/claim match at a human review gate, when, and what decision was made.

## Files

- `source-record.schema.json` — required metadata for sources.
- `claim-record.schema.json` — required metadata for claim-level evidence cards.
- `contradiction-search-record.schema.json` — provenance for current-evidence contradiction/supersession searches.
- `review-event.schema.json` — provenance for actual human review.
- `sources.json` — initial source registry.
- `sources-2026-09-16.json` — append-only current-evidence source shard added during the flagship contradiction search.
- `claims.json` — initial claim cards linked to source IDs.
- `contradiction-searches.json` — machine-readable search records covering CLM-0001 through CLM-0009.
- `review-events.json` — human review registry; intentionally empty until actual review occurs.
- `FLAGSHIP_CONTRADICTION_SEARCH_2026-09-16.md` — narrative audit explaining current evidence and claim-level calibration.
- `WORKFLOW.md` — citation verification, contradiction search, correction, and publication workflow.

## Why source shards exist

New evidence should be appendable without rewriting a large historical registry merely to add a current source. Source IDs must remain globally unique across shards, and CI validates cross-shard duplication and contradiction-search references.

A dated source shard does **not** create a different evidence standard. Every record still uses the same source metadata/state rules and remains subject to human review.

## Evidence labels

HOSI uses its educational A–E labels:

- **A — High confidence**
- **B — Moderate confidence**
- **C — Limited/mixed**
- **D — Emerging/preliminary**
- **E — Insufficient**

These labels apply to a **specific claim**, not permanently to an entire paper, author, guideline, treatment, diagnosis, or institution.

## Verification states

A source record may be:

- `discovered`
- `metadata_verified`
- `full_text_checked`
- `human_reviewed`
- `superseded`
- `retracted`
- `withdrawn`

A claim may be:

- `draft`
- `source_matched`
- `contradiction_searched`
- `human_reviewed`
- `approved_for_curriculum`
- `held`
- `superseded`

No AI may set `human_reviewed` or `approved_for_curriculum` unless an actual human review event is recorded.

## Contradiction-search states

A current-evidence search may record:

- `no_material_conflict_found`
- `mixed_or_qualifying_evidence_found`
- `material_conflict_found`
- `superseded`

`No material conflict found` is **not** a declaration that the literature is complete, unanimous, or proven true. It means the documented search did not identify evidence requiring reversal of that bounded claim.

The dated flagship search currently covers all nine initial claims. Every record intentionally retains `human_full_text_review_pending=true`.

## Dates

The library distinguishes:

- `published_year` — when the source was published.
- `source_last_updated` — when the publisher/guideline owner says it was updated, if known.
- `verified_on` — when HOSI last checked the source metadata/status.
- `next_review_due` — when HOSI intends to re-check it.
- `searched_on` — when a contradiction/supersession search was performed.

An old guideline can still be current. A new paper can still be weak. The calendar is not an evidence rating system, despite humanity's recurring attempts to use it as one.

## Current flagship-search result

The 2026-09-16 AI-assisted search found **no initial claim requiring wholesale reversal**, largely because the claims were deliberately narrow. It did identify important calibration:

- distributed cognition is broad but not literally ubiquitous;
- the sleep two-process model remains useful while being actively refined;
- CBT remains guideline-supported for adult MDD but treatment choice remains contextual;
- IPSRT remains a recognized adjunctive bipolar psychotherapy without evidence that it universally outranks other named psychotherapies;
- multimodal bipolar-care framing remains supported;
- ADHD rating scales are useful aids, not standalone diagnoses;
- newer OCD evidence continues to support ERP with population/comparator/format caveats;
- APA 2025 adds a current cross-guideline source for PTSD treatment literacy;
- current CDC plus VA/DoD sources reinforce mTBI variability and individualized-prognosis boundaries.

These are AI-assisted search findings, not completed human full-text audit decisions.

## Automated QA

Research Library CI runs:

1. `validate_research_library.py` for the core source/claim/review registry.
2. `validate_research_contradiction_searches.py` for supplemental source shards and flagship contradiction-search provenance.

The second validator requires:

- globally unique source IDs across the initial and dated source shards;
- valid source metadata/state values;
- valid claim/source references;
- one documented flagship search for each CLM-0001 through CLM-0009;
- valid search result/action states;
- `human_full_text_review_pending=true` until a real human review process changes that state elsewhere.

A green check proves structural/provenance consistency, not scientific truth or peer review.

## Publication boundary

Records in this library are research infrastructure, not medical advice, diagnosis, accreditation, or treatment instructions. Curriculum publication still requires the applicable human academic, clinical/safety, lived-experience, accessibility, and assessment gates.