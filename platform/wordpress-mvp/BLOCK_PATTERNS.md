# HOSI WordPress.com Free — Native Block Recipes

These recipes use native WordPress.com editor features and do not require plugins.

The exact visual controls vary by theme. Preserve semantics/accessibility even when styling differs.

## 1. Global header

Recommended blocks:

1. Site Logo / Site Title
2. Navigation
3. Search

Primary navigation:
- Start Here
- Colleges
- Courses
- Study Paths
- Research Library
- Evidence Guide
- About HOSI

Keep the menu short on mobile. Put policies/corrections/accessibility/contact in the footer.

## 2. Homepage hero

Blocks:
- Group
- Heading (H1): `Human Operating System Institute`
- Paragraph: `Learn the Operating System Before the Diagnosis.`
- Paragraph: concise mission
- Buttons:
  - `Start Here`
  - `Explore HOSI-101`
  - `How HOSI Handles Evidence`

Avoid autoplay animation and moving backgrounds.

## 3. “What HOSI is” principles grid

Use a Columns or Grid layout if available; ensure the mobile stack remains logical.

Cards:
- Person-first
- Systems-first
- Evidence-first
- Accessible
- Revisable
- Explicit about uncertainty

Each card should have a heading, not merely bold decorative text.

## 4. Search panel

Use the native **Search block**.

Label:
`Search HOSI lessons and pages`

Helper text:
`Search uses titles and page/post body text. Try terms such as working memory, sleep, ERP, or research literacy.`

Do not imply WordPress search is a scientific database search.

## 5. Course index with Query Loop

Use a **Query Loop** filtered to category `HOSI-101`.

Post Template should show:
- Post Title
- Excerpt
- Modified Date where supported
- module/category context where the chosen theme exposes it

Sort in a deliberate lesson sequence if the native query/theme supports the needed ordering. If reliable numeric ordering is not available without code/plugin support, maintain a manually curated module index page rather than pretending chronological order is course order.

## 6. Module index

For each 10-lesson module:

- Heading: module number/name
- short module purpose
- evidence/review note
- manually maintained ordered list of Lessons 1–10 within the module
- Query Loop below the ordered list as a discovery/recent-update aid if useful

The manually curated ordered list is the canonical sequence on Free.

## 7. Evidence-status banner

Use a Group block with:

**Heading:** `Evidence & review status`

Fields:
- Publication state
- Evidence level
- Last reviewed date
- Last revised date
- Human review state
- Canonical source link

Example:

> **Human review pending.** This manuscript has source records and automated structural QA, but applicable independent human review is not complete. It is not public final curriculum.

Color must not be the only way the status is communicated.

## 8. Evidence map

Use a Table block with columns:
- Claim
- HOSI evidence level
- Source family
- Important limitation

Keep the table narrow enough for mobile; when content is long, use stacked headings/paragraphs instead of creating a horizontal-scroll nightmare because apparently tables enjoy punishing phones.

## 9. Condition-specific application panel

Use a Group block:

**Heading:** `Condition-specific application`

Start with:
`This section applies the general system to a diagnostic context. It does not mean the system behaves the same way in every person with this diagnosis.`

## 10. Combination/comorbidity panel

Use a Group block with an explicit evidence-density statement:

- Direct evidence
- Indirect/extrapolated evidence
- Limited/mixed evidence
- Not established

Do not present every combination pathway as equally studied.

## 11. Lived-experience panel

Heading:
`Lived-experience perspective`

Visible note:
`Lived experience can illuminate meaning, burden, usability, stigma, and everyday function. It is kept distinct from population-level causal or treatment-efficacy claims.`

## 12. Knowledge check + answer explanation

Use Heading + List/Paragraph questions.

For each answer, use a native **Details block**:

Summary:
`Check the answer and reasoning`

Hidden content:
- correct answer
- explanation
- evidence caveat

This gives a useful self-check on Free without claiming authenticated grading.

## 13. Sensitive reflection

Use a Group block with text before the prompt:

> **Disclosure is optional.** You may answer with a fictional example, a general observation, or skip this reflection. Personal trauma, diagnosis, treatment history, or private information is not required to complete HOSI coursework.

Never embed a public comment request asking learners to disclose sensitive answers.

## 14. Research-update log

Use Table or List:
- date
- change
- reason
- review state

Link material corrections to the Corrections & Updates page.

## 15. “What would change our mind?” block

Use a distinct Heading and paragraph/list.

Purpose:
- model scientific revisability
- expose falsifiability/decision thresholds
- prevent “published” from becoming “permanently unquestionable”

## 16. Previous / next navigation

Use Navigation, Buttons, or Paragraph links:

`← Previous lesson`  
`Module index`  
`Next lesson →`

Then:
- Course index
- Evidence Guide
- Corrections & Updates

## 17. Study-path landing page

Build with:
- title
- plain-language purpose
- explicit non-diagnostic statement
- recommended starting lessons
- relevant lesson list
- evidence-density note for combination pathways

Do not ask visitors to select their diagnosis as a required onboarding step.

## 18. Colleges page

Use headings/cards for the ten core colleges:
1. College of Human Operating Systems
2. College of Bipolar Studies
3. College of ADHD Studies
4. College of OCD Studies
5. College of Trauma & PTSD Studies
6. College of Brain Injury Studies
7. College of Cognitive & Behavioral Therapies
8. College of Research Literacy
9. College of Human Self-Management
10. College of Ethics, Philosophy & Stewardship

Each card links to educational content, not a claim of accreditation.

## 19. Research Library public page

On the $0 public campus, this is an **explainer/index**, not the private or machine-readable research backend.

Show:
- evidence-rating guide
- public source cards approved for display
- correction policy
- link to canonical GitHub research records

Do not expose private reviewer notes, credentials, or sensitive data.

## 20. Atlas public page

Public informational page only until the privacy-safe Atlas backend is production-ready.

Show:
- what Atlas is
- author ownership
- privacy principles
- AI boundaries
- development status

Do not use ordinary WordPress comments/forms to collect private Atlas reflections.
