# HOSI-101 Lessons 001–020 — QA Record

**Scope:** Module 01 — Orientation; Module 02 — Neuroscience Foundations  
**Branch:** `curriculum/hosi101-lessons-01-20`  
**PR:** #11  
**QA date:** 2026-09-16  
**Current manuscript state:** source-verified drafts; independent human review pending

## What was validated

The deterministic validator `scripts/validate_hosi101_01_20.py` checks the exact canonical 001–020 block for:

- exactly 20 individual manuscript files and the expected IDs;
- canonical lesson ID/filename consistency;
- required draft/review metadata;
- 26 numbered lesson sections;
- original visual brief and accessible alt text;
- explicit non-diagnostic safety/scope boundary in every manuscript;
- A–E evidence-confidence markers for substantive lessons;
- assessment scaffold;
- references or canonical source-registry pointer;
- explicit `What would change our mind?` revision trigger;
- block-level source registry and evidence audit;
- human-review packet with 20 pending lesson decisions;
- canonical course manifest preserving 200 planned lessons / 20 modules;
- explicit `not_published` state for the 001–020 block.

## QA history

### Initial PR run

The initial run correctly inspected all 20 manuscripts but failed 15 checks. Fourteen failures came from safety-boundary detection and one from the Module 02 review lesson’s legitimate `Integrated neuroscience model` section heading.

Review showed that many manuscripts already contained meaningful safety constraints, but the first validator version required overly narrow stock diagnostic wording. The validator was repaired to recognize semantically equivalent explicit diagnostic prohibitions, while continuing to require a diagnostic boundary inside each lesson’s Safety / scope section.

### Second validation pass

After the semantic parser repair, six lessons still failed because their safety sections constrained treatment, experiments, recovery, or clinical interpretation but did **not** explicitly state a non-diagnostic boundary:

- HOSI-101-006 — How Learning Changes the Brain
- HOSI-101-007 — The Scientific Method
- HOSI-101-008 — Understanding Evidence
- HOSI-101-015 — The Brainstem
- HOSI-101-017 — Neuroplasticity
- HOSI-101-019 — Brain Health Across the Lifespan

Those were treated as manuscript defects rather than weakening the validator. Each lesson was revised to explicitly prohibit diagnostic inference from classroom exercises, evidence ratings, symptoms, apparent learning/plasticity, or risk factors as appropriate.

### Passing run

**GitHub Actions workflow:** `HOSI-101 Lessons 01-20 QA`  
**Run:** #8  
**Run ID:** `35074604132`  
**Job:** `Validate canonical Lessons 001-020`  
**Job ID:** `104723890847`  
**Validated head:** `b3ee02593888c6ec76af4ea9350dda15008d0aa2`  
**Conclusion:** **SUCCESS**

All workflow steps completed successfully, including the deterministic Lessons 001–020 QA step.

## Evidence / overclaim audit status

`research/HOSI101_Lessons_01-20_EVIDENCE_AUDIT_2026-09-16.md` records the AI-assisted lesson-by-lesson evidence and overclaim audit. That audit found no draft requiring wholesale reversal during this cycle, while preserving material qualifications around:

- regional specialization versus distributed cognition;
- historical versus modern limbic-system framing;
- established versus unsettled cerebellar roles;
- connectivity versus causality;
- constrained neuroplasticity and recovery;
- developmental variability and anti-determinism;
- population risk reduction versus individual prevention guarantees.

## Human-review state

All human review decisions remain **Pending** in `review/HOSI101_01-20_HUMAN_REVIEW_PACKET.md`.

A green QA run does **not** establish:

- scientific truth or full-text source approval;
- subject-matter peer review;
- medical or clinical safety approval;
- lived-experience approval;
- accessibility approval;
- assessment validity;
- publication approval;
- accreditation or certification authority;
- completion of the entire 200-lesson HOSI-101 course.

## Exit boundary

The AI-side manuscript-production, evidence-audit, repository-consistency, and deterministic-QA work for Lessons 001–020 is complete for this draft cycle.

The block must remain a draft until applicable qualified human review, correction/re-review, final reviewed-head QA, and explicit human merge/release decisions occur.
