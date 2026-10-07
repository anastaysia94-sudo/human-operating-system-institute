# HOSI Human Review Packets

Use these packets to record qualified human review. They are templates, not evidence that review occurred.

## 1. Subject-matter review

Reviewer should verify:
- factual accuracy for the relevant discipline;
- terminology is current and appropriately scoped;
- mechanism claims are not overstated as clinical outcomes;
- population limits and uncertainty are visible;
- condition labels are not treated as complete explanations of a person;
- ordinary human-system baselines precede pathology where appropriate;
- material conflicts with current major guidance are identified.

Required output: pass / pass with notes / changes required / reject, plus citations or rationale for material changes.

## 2. Citation / claim-to-source audit

For every material scientific or clinical claim sampled or reviewed:
- identify the exact claim;
- identify the exact source(s);
- confirm the source actually supports the wording used;
- verify bibliographic fields and DOI/URL where applicable;
- record population, design, comparator, outcomes and limitations;
- search for newer systematic reviews/guidelines where appropriate;
- search for meaningful contradictory or superseding evidence;
- distinguish metadata verification from full-text review;
- downgrade or narrow claims when evidence is indirect, heterogeneous or outdated.

Do not approve a citation because the title merely sounds relevant. Humanity has invented abstracts for a reason.

## 3. Medical / safety review

For health, psychiatric, neurological, trauma or treatment content:
- confirm educational scope is clear;
- identify dangerous omissions or misleading simplifications;
- confirm no start/stop/change-medication instruction is presented as personal medical advice;
- confirm urgent danger signs, where discussed, defer to appropriate professional/emergency care;
- confirm no diagnosis is inferred from a quiz, app score, isolated symptom or Atlas reflection;
- confirm treatment descriptions preserve choice, uncertainty and appropriate professional context;
- check medication/pharmacology language for both benefit and risk framing rather than blanket advocacy or opposition.

## 4. Lived-experience review

Reviewer should evaluate whether material:
- avoids moralizing, stereotyping or identity reduction;
- distinguishes lived testimony from population-level evidence;
- offers non-disclosure alternatives for sensitive exercises;
- avoids forced trauma disclosure;
- avoids treating memory confidence as factual verification;
- avoids suggestive memory-recovery methods;
- represents meaningful variation within diagnostic groups;
- names uncertainty where scientific categories do not match lived experience cleanly.

A lived-experience reviewer is not required to disclose their own diagnosis or history in the review record.

## 5. Accessibility review

Review the rendered artifact, not only source Markdown.

Check:
- keyboard-only navigation;
- visible focus;
- heading order and landmarks;
- link purpose;
- alt text for informative visuals;
- decorative-image handling;
- captions/transcripts for media;
- color contrast and no color-only meaning;
- zoom/reflow/mobile behavior;
- screen-reader reading order;
- cognitive load, chunking and plain-language alternatives;
- form labels/error recovery where forms exist;
- non-disclosure alternatives in assignments;
- accessible document/export formats.

Record actual devices/browsers/assistive technologies used when applicable.

## 6. Assessment / rubric review

Check that assessments:
- measure stated learning objectives;
- do not covertly assess disclosure, treatment choice or ideological agreement;
- have defensible answer keys/rubrics;
- distinguish formative self-checks from secure graded assessment;
- include accommodations/alternative response paths where appropriate;
- do not convert educational scores into diagnostic claims;
- identify ambiguity or multiple defensible answers;
- include appeal/correction handling before credential use.

## 7. Privacy / security review

For Atlas, accounts or private learner data, verify:
- private-by-default access;
- server-side authorization, not client-only hiding;
- cross-user isolation;
- purpose-specific consent;
- AI provenance and approval states;
- export, correction, unsharing and deletion flows;
- log/telemetry minimization;
- secret management;
- backup/deletion semantics;
- incident response;
- prompt-injection boundaries;
- no silent diagnostic or clinical-risk profiling.

## Reviewer record

Every completed packet must create a `review-event` record referencing the exact artifact/version reviewed. A checked Markdown box without provenance does not satisfy a human gate.