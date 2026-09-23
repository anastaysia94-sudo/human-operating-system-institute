# HOSI Public Beta Checklist

**Default state: NOT RELEASE-APPROVED.**

This checklist is a release-control surface, not evidence that review happened. Boxes may be checked only from actual supporting records.

## Scope and version
- [ ] Release candidate has a unique version/tag or immutable Git SHA.
- [ ] Included courses/features are explicitly listed.
- [ ] Known excluded/incomplete features are listed.
- [ ] Public status labels match repository state.

## Academic / evidence
- [ ] Applicable subject-matter review events pass.
- [ ] Applicable claim-to-source/citation audit events pass.
- [ ] Contradictory/superseding evidence searches are complete for high-impact claims.
- [ ] Evidence labels match the reviewed claim scope.
- [ ] Material scientific corrections are resolved and re-reviewed.

## Safety / lived experience
- [ ] Applicable medical/safety review events pass.
- [ ] Applicable lived-experience review events pass.
- [ ] Trauma-sensitive material has non-disclosure alternatives.
- [ ] No suggestive memory-recovery exercise is present.
- [ ] No quiz/app/Atlas reflection is presented as diagnostic.
- [ ] Medication content avoids individualized start/stop/change instructions.

## Accessibility
- [ ] Rendered keyboard test completed.
- [ ] Screen-reader/semantic review completed for public critical flows.
- [ ] Mobile/reflow/zoom reviewed.
- [ ] Color is not the sole carrier of meaning.
- [ ] Images/media have appropriate alternatives.
- [ ] Known accessibility blockers are resolved or release-blocking.

## Platform / privacy / security
- [ ] Public campus URLs verified logged out.
- [ ] No private Atlas data is exposed in public systems.
- [ ] Authentication/authorization tests pass where accounts/private data exist.
- [ ] Cross-user isolation is tested where accounts/private data exist.
- [ ] Export/delete/correction flows are tested where private data exist.
- [ ] Secrets are not committed to public source.
- [ ] Incident-response owner/process exists before private-data pilot.

## AI / Atlas
- [ ] Applicable AI red-team cases executed.
- [ ] Blocking AI red-team failures resolved and retested.
- [ ] AI output is distinguishable from user-authored/accepted narrative.
- [ ] Research use requires separate consent.
- [ ] No covert diagnosis or silent clinical-risk profile is created from educational reflections.

## Learner pilot
- [ ] Pilot protocol version recorded.
- [ ] Participant privacy/consent rules applied.
- [ ] Critical navigation/comprehension problems resolved.
- [ ] Severe accessibility blockers resolved.
- [ ] Repeated diagnostic/treatment misinterpretations addressed.
- [ ] Human pilot-review event recorded.

## Corrections / release engineering
- [ ] No open critical correction exists in release scope.
- [ ] Major corrections are resolved or explicitly release-blocking.
- [ ] Automated QA passes on the exact release candidate.
- [ ] Release notes list known limitations.
- [ ] Rollback/correction path is documented.

## Final human decision
- [ ] Authorized human release decision is recorded as a review event.
- [ ] Release event references the exact candidate SHA/tag.
- [ ] Public wording uses `public beta` or the approved status, not `final`, unless final-release governance has separately passed.

A green CI run may verify that the checklist and registries are structurally consistent. It may **not** check the final human-decision box.