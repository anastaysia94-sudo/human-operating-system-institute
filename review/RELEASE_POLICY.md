# HOSI Versioned Release Policy

## Purpose

HOSI releases must make it possible to answer: what exactly was released, what review state did it have, what evidence supported it, what changed later, and who authorized the release.

## Release classes

### Draft
Work in development. May be useful internally. Not represented as reviewed or published.

### Review candidate
Stable enough for structured human review. Content may still change materially.

### Public beta
Approved for limited public use with explicit known limitations and a correction path. Public beta is not `final`.

### Published
Approved for normal public educational use under the applicable governance scope. Publication does not make the content permanently correct; correction and supersession remain active obligations.

### Superseded
A newer version replaces the artifact for current use. Historical records remain traceable.

## Version record

Every release candidate should identify:
- semantic or project version;
- Git tag and/or immutable commit SHA;
- release date;
- included artifacts/features;
- excluded/incomplete scope;
- applicable review gates;
- review event IDs;
- open known limitations;
- correction IDs affecting the candidate;
- automated QA run/reference;
- human release-decision review ID.

## Status integrity

Do not infer status from file existence, branch name, merged PR count, automated test success, or AI-generated summaries.

The words `reviewed`, `peer reviewed`, `clinically reviewed`, `accessibility approved`, `release approved`, `published`, and `final` must correspond to the specific governance state claimed.

## Corrections

Material corrections should preserve:
- the prior version;
- the corrected version;
- a correction record describing what changed and why;
- source/evidence when applicable;
- re-review where the correction affects a reviewed claim or safety decision.

Do not silently rewrite material scientific claims on a public release without a visible correction/update trail.

## Rollback

A release may be withdrawn or rolled back when:
- critical scientific misinformation is identified;
- a safety defect is identified;
- private data exposure occurs;
- authorization/cross-user isolation fails;
- a credential claim is invalid;
- an AI feature violates consent or non-diagnostic boundaries;
- severe accessibility barriers make a critical flow unusable.

Rollback does not erase the incident. Record the affected version and corrective action.

## Final authority

Only an authorized human release decision may advance a candidate to public beta or published status. CI may block release but may not approve it.