# HOSI Public Campus — Accessibility Checklist

Use before public release of a page, lesson, assessment, downloadable asset, or major template change.

This is a product QA checklist, not a claim of formal WCAG conformance or third-party accessibility certification.

## Structure

- [ ] One clear H1 for the page/lesson.
- [ ] Heading levels follow a logical hierarchy; headings are not chosen only for visual size.
- [ ] Lists use actual list blocks.
- [ ] Tables are used for tabular data, not page layout.
- [ ] Link text identifies the destination or purpose without relying on “click here.”
- [ ] Navigation labels remain consistent across the campus.

## Keyboard

- [ ] All interactive elements can be reached by keyboard.
- [ ] Focus order follows reading order.
- [ ] Visible focus is not removed by styling.
- [ ] Details/collapsible answer sections are keyboard operable.
- [ ] No interaction requires hover only.

## Images and visual content

- [ ] Informative images have useful alt text.
- [ ] Decorative images are marked appropriately so they do not create screen-reader noise.
- [ ] Charts/diagrams have equivalent text explanations when needed.
- [ ] Scientific claims do not depend on a decorative image.
- [ ] Existing asset provenance is retained in the repository/asset register.

## Color and status

- [ ] Status is communicated in words, not color alone.
- [ ] Evidence ratings are written as text, not only colored badges.
- [ ] Text/background contrast is checked in the selected theme.
- [ ] Links can be recognized without requiring color perception alone.

## Mobile

- [ ] Page works at narrow phone width without required horizontal scrolling.
- [ ] Tables are simplified or restructured when they become unusable on mobile.
- [ ] Buttons/touch targets are comfortably tappable.
- [ ] Primary actions do not sit too close together.
- [ ] Sticky/fixed elements do not cover reading content.

## Text and cognitive accessibility

- [ ] Opening paragraph explains what the page is for.
- [ ] Jargon is defined near first use.
- [ ] Long sections use meaningful headings.
- [ ] Instructions are short and sequential.
- [ ] Key safety/scope statements are not hidden in footnotes.
- [ ] Evidence uncertainty is stated plainly.
- [ ] Learners can skip sensitive reflection prompts.
- [ ] Personal disclosure is never required merely to demonstrate concept mastery.

## Assessments

- [ ] Knowledge-check instructions distinguish learning activity from diagnosis/screening.
- [ ] Answers/rationales explain reasoning, not merely “right/wrong.”
- [ ] Time pressure is not introduced without a legitimate learning purpose.
- [ ] Formal future assessments have an accommodation route.
- [ ] The rubric does not grade beliefs, treatment preferences, disability identity, diagnosis, or willingness to disclose private material.

## Trauma-sensitive content

- [ ] Page provides scope/content context before potentially distressing material.
- [ ] Reflection/discussion has a non-personal or fictional alternative.
- [ ] No exercise pressures memory recovery or trauma disclosure.
- [ ] Safety language does not sensationalize trauma.
- [ ] Emergency/clinical deferral is used where actually relevant, not pasted onto every paragraph until it becomes wallpaper.

## Video/audio when introduced

- [ ] Captions are available for meaningful speech.
- [ ] Transcript is available where appropriate.
- [ ] Autoplay is avoided.
- [ ] Controls are accessible.
- [ ] Visual-only information has verbal/text equivalent when necessary.

## Downloads

- [ ] Filename is descriptive.
- [ ] File format is identified.
- [ ] PDF/DOCX accessibility is reviewed independently before calling the file accessible.
- [ ] Critical course content is not locked exclusively inside an inaccessible download.

## Search/navigation

- [ ] Lesson title contains the canonical concept name learners would search for.
- [ ] Important vocabulary appears in body text because WordPress native Search does not search category/tag labels as content.
- [ ] Previous/module/next/course links are present where applicable.
- [ ] Unpublished destinations are not presented as normal working lesson links.

## Review record

For every formal accessibility review, record:
- page/lesson ID
- URL or repository source
- reviewer
- review date
- device/browser/assistive technology when relevant
- blocking issues
- correction commit/version
- re-test result

Do not pre-check this list from AI generation alone. Accessibility review requires actual rendered-content testing.
