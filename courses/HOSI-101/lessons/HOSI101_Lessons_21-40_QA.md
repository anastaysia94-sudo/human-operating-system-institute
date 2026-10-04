# HOSI-101 Lessons 21–40 — Draft QA Record

**QA date:** 2026-09-06  
**Branch:** `curriculum/hosi101-lessons-21-40`  
**Scope:** automated/AI-assisted structural and repository-state QA only  
**Not claimed:** independent academic review, clinical review, accessibility certification, peer review, learner pilot, or publication approval

## Automated structural checks

A local deterministic check inspected the 20 generated lesson manuscripts (`HOSI101_Lesson_021.md` through `HOSI101_Lesson_040.md`) for the required lesson architecture and false completion language.

**Result: PASS — 20 lessons checked, 0 structural failures.**

Required elements checked included:

- Original visual / cover brief
- Accessible alt text
- Why this matters
- Learning objectives
- Vocabulary
- Normal human-system baseline
- Core science
- Evidence map
- What is uncertain
- Condition-specific applications
- Combination/comorbidity panel
- Lived-experience perspective
- Practical skill / exercise
- Safety / scope
- Cornell Notes
- Reflection
- Discussion prompt
- Knowledge check / quiz
- Homework
- Instructor answer key / rubric
- References
- Research update log
- “What would change our mind?”

The check also verified that each local manuscript retained an **independent human review pending** marker and did not contain false status claims such as `Published`, `Reviewed`, `100% complete`, or `independent peer review complete`.

## Repository comparison check

GitHub comparison of `main` to `curriculum/hosi101-lessons-21-40` returned:

- branch status: ahead
- behind by: 0
- lesson files added: 20 (`021`–`040`)
- source registry added: 1
- course/status documentation corrected: 2

This confirms the branch was built from the inspected `main` state rather than overwriting unrelated work.

## Evidence QA performed in this pass

- Public PubMed, NIMH, and CDC source pages used in the lesson set were checked during the draft pass.
- The source registry records 23 sources and distinguishes source metadata verification from full claim verification.
- Evidence labels are attached to claims and are not treated as permanent grades for an entire source.
- Lesson 30's reinforcement-learning citation was corrected so computational reinforcement-learning claims are not supported only by a habit-review source.
- Lessons 38–39 include heightened scope/safety controls for trauma memory and brain injury.

## Sensitive-content safeguards checked

The trauma-memory and brain-injury lessons explicitly avoid:

- diagnosing learners
- forced disclosure
- suggestive “memory recovery” exercises
- treating memory confidence as factual verification
- individualized TBI prognosis or clearance decisions
- substituting coursework for qualified clinical, rehabilitation, or emergency care

## Remaining mandatory human gates

This QA record does **not** close Issue #1 or authorize publication. Before merge/publication/final certification use, the applicable work still requires:

- [ ] Full-text claim-to-source citation audit
- [ ] Search for newer and contradictory evidence
- [ ] Subject-matter review
- [ ] Medical/safety review where applicable
- [ ] Lived-experience review where applicable
- [ ] Accessibility review by a qualified human reviewer/user testing
- [ ] Assessment and instructor-rubric review
- [ ] Correction pass
- [ ] Human pull-request approval
- [ ] Merge/release decision

## Release statement

**QA disposition: suitable for draft pull-request review; not suitable to label Published, peer reviewed, clinically reviewed, accredited, or production complete.**
