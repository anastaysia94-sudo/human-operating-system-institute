# HOSI Research Library MVP

This directory is the machine-readable evidence layer for the Human Operating System Institute.

It does **not** turn a citation into a verified claim merely because a URL resolves. HOSI keeps three separate objects:

1. **Source record** — what the publication/guideline/resource is.
2. **Claim record** — the exact educational or clinical claim HOSI wants to make.
3. **Review event** — who checked the source/claim match, when, and what changed.

## Files

- `source-record.schema.json` — required metadata for sources.
- `claim-record.schema.json` — required metadata for claim-level evidence cards.
- `sources.json` — initial verified source registry.
- `claims.json` — initial claim cards linked to source IDs.
- `WORKFLOW.md` — citation verification, contradiction search, correction, and publication workflow.

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

## Dates

The library distinguishes:

- `published_year` — when the source was published.
- `source_last_updated` — when the publisher/guideline owner says it was updated, if known.
- `verified_on` — when HOSI last checked the source metadata/status.
- `next_review_due` — when HOSI intends to re-check it.

An old guideline can still be current. A new paper can still be weak. The calendar is not an evidence rating system, despite humanity's recurring attempts to use it as one.

## Publication boundary

Records in this library are research infrastructure, not medical advice, diagnosis, accreditation, or treatment instructions. Curriculum publication still requires the applicable human academic, clinical/safety, lived-experience, accessibility, and assessment gates.
