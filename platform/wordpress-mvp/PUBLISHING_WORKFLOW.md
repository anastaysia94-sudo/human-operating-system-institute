# HOSI GitHub → WordPress Publishing Workflow

## Principle

GitHub is the canonical curriculum and evidence source. WordPress.com is the public presentation layer.

A WordPress page must not become more confident than the reviewed GitHub source it represents.

## Status flow

`architecture_outline`  
→ `draft`  
→ `human_review_pending`  
→ `reviewed_for_publication`  
→ `published`

Side states:
- `correction_pending`
- `superseded`

Automation may validate structure, but only a documented human approval can move content through a human-review gate.

## 1. Select candidate content

Candidate source must identify:
- lesson/page ID
- canonical repository path
- current Git commit/version
- review state
- applicable evidence record(s)
- applicable safety/accessibility review state

Do not publish directly from an old transfer packet merely because it sounds finished.

## 2. Verify review gates

For a scientific/clinical lesson, check the applicable gates:
- subject-matter review
- citation/evidence audit
- clinical/safety review where applicable
- lived-experience review where applicable
- accessibility/content review
- assessment/rubric review
- correction resolution

If a gate is not required for that content, record `not applicable` with rationale rather than pretending it passed.

## 3. Freeze publication source

Record the exact Git commit SHA used for the WordPress publication.

The public lesson metadata should link to the canonical source or public repository location when appropriate.

## 4. Transform for WordPress

Use `LESSON_TEMPLATE.md`.

Preserve:
- evidence labels
- uncertainty
- references
- safety/scope
- research update log
- revision date
- “What would change our mind?”

Do not omit uncertainty because it makes the page shorter or prettier.

## 5. Apply taxonomy

Categories:
- `HOSI-101`
- exact module category

Tags:
- relevant study paths
- relevant human systems

Keep combined taxonomy focused. Do not perform SEO keyword confetti by attaching every diagnosis to every lesson.

## 6. Configure navigation

Update:
- module ordered list
- course index
- previous lesson
- next published lesson
- study-path links where relevant

Avoid dead “next” links to material that is not publicly available.

## 7. Add evidence status

Every lesson visibly states:
- publication state
- evidence level
- last reviewed date
- last revised date
- canonical source

If content is published while a correction is pending, show that status prominently and link to the correction record.

## 8. Accessibility QA

Use `ACCESSIBILITY_CHECKLIST.md` on the rendered WordPress page.

Check actual mobile and keyboard behavior. A Markdown source passing a linter does not prove the theme rendered it accessibly.

## 9. Preview

Before public publication:
- inspect desktop
- inspect narrow mobile
- test keyboard navigation
- test Search discoverability
- test previous/next links
- test Details answer blocks
- verify references/DOIs/URLs
- verify image alt text
- verify no draft/private notes leaked

## 10. Publish

Only after the applicable gate record says publication is approved.

Record:
- public URL
- publication date/time
- WordPress author/editor account
- source Git SHA
- WordPress revision/version if available

## 11. Post-publication verification

Confirm as a logged-out visitor:
- public URL works
- no editor-only controls/content appear
- search/index navigation works
- lesson is in correct module/course category
- mobile layout is readable

## 12. Corrections

When a material error is found:

1. Create/identify the correction issue.
2. Mark public lesson `Correction pending` if warranted.
3. Correct the canonical GitHub source first when practical.
4. Review the correction.
5. Update WordPress.
6. Record old/new versions and date.
7. Remove `Correction pending` only when resolved.

Do not silently edit substantive scientific mistakes with no correction trail.

## 13. Supersession

If a lesson is replaced:
- mark old public page `Superseded`
- link clearly to replacement
- preserve revision history as policy allows
- prevent old content from looking like the preferred current lesson

## 14. Research Library updates

A changed source does not automatically force every linked lesson to change, but it should trigger claim-level impact review.

Track:
- source superseded/retracted/corrected
- affected claim IDs
- affected lesson IDs
- review decision

## 15. Platform-feature verification

Re-check current WordPress.com official documentation before stating:
- pricing
- plugin availability
- storage
- domain benefits
- plan-specific functionality

Platform rules change. Do not turn a 2026 support page into a geological constant.

## Publication record template

```text
Content ID:
Public title:
Canonical repo path:
Source Git SHA:
Public status:
Evidence level:
Human review record(s):
Accessibility review:
Safety review:
WordPress URL:
Published at:
Published by:
Last verified logged-out:
Correction/supersession state:
```
