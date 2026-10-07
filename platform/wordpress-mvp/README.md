# HOSI WordPress.com $0 Campus MVP

**Issue:** #4 — HOSI WordPress/LMS MVP  
**Platform target:** WordPress.com Free first  
**Canonical curriculum source:** GitHub repository  
**Verification date for platform capabilities:** 2026-09-15

## Goal

Launch the lowest-cost credible public HOSI campus without pretending WordPress.com Free is a full LMS.

The free campus provides public educational publishing, course navigation, search, taxonomies, evidence-status displays, accessible self-checks, and a learner-controlled manual progress workflow. Persistent individual progress, authenticated assessments, automated grading, certificates, enrollment, and private Atlas data remain later LMS/backend requirements.

## Current official WordPress.com capability baseline

Verified against current WordPress.com documentation in September 2026:

### Available on Free
- WordPress.com hosting
- free WordPress.com site address
- 1 GB media storage
- unlimited pages and posts
- unlimited site users/contributors
- mobile-ready themes
- WordPress block editor
- Search block
- categories and tags
- Query Loop for filtered/dynamic post listings
- Details block for collapsible answer/explanation sections
- built-in security/anti-spam/platform maintenance features

### Not available on Free
- installing third-party WordPress plugins
- setting a custom domain as the primary site address
- plugin-dependent LMS functionality

Plugin installation is currently available on WordPress.com paid plans. A custom domain can become the primary site address with a paid plan. Therefore the $0 MVP must not claim LearnDash/Tutor LMS/plugin functionality or a custom primary domain.

Official references:
- https://wordpress.com/free/
- https://wordpress.com/support/plan-features/
- https://wordpress.com/support/plugins/install-a-plugin/
- https://wordpress.com/support/domains/set-a-primary-address/
- https://wordpress.com/support/wordpress-editor/blocks/search-block/
- https://wordpress.com/support/wordpress-editor/blocks/query-loop-block/
- https://wordpress.com/support/posts/categories/
- https://wordpress.com/support/posts/tags/
- https://wordpress.com/support/wordpress-editor/blocks/details-block/

## Public-campus information architecture

Top-level pages:

1. Home
2. About HOSI
3. Colleges
4. Courses
5. HOSI-101 — Understanding the Human Operating System
6. Research Library
7. Founder's Atlas
8. Policies
9. Accessibility
10. Contact

Supporting utility pages:
- Start Here
- Evidence Guide
- Study Paths
- Curriculum Status
- Corrections & Updates

## WordPress content model

### Pages
Use Pages for durable institutional/navigation content:
- Home
- About
- Colleges
- Courses index
- Research Library explainer
- Atlas explainer
- Policies
- Accessibility
- Contact
- Start Here

### Posts
Use Posts for individual lesson publications because WordPress categories/tags and Query Loop can create scalable course/study-path indexes without plugins.

Each published lesson post receives:
- one course category, e.g. `HOSI-101`
- one module category, e.g. `Module 03 — Learning & Memory`
- optional study-path tags such as `ADHD`, `OCD`, `PTSD`, `Brain Injury`, `Research Literacy`
- human-system tags such as `working memory`, `sleep`, `attention`, `emotion regulation`
- evidence-state tag controlled by the publishing workflow

Do not use taxonomy as a diagnostic profile of the visitor.

## Status vocabulary

Public content must use one of these visible states:

- **Architecture / outline** — structure exists; not a lesson manuscript.
- **Draft** — manuscript exists; publication/review gates incomplete.
- **Human review pending** — substantive draft with applicable human review still outstanding.
- **Reviewed for publication** — applicable review gates documented and approved.
- **Published** — deliberately released to the public campus after review.
- **Correction pending** — published material has a known issue under review.
- **Superseded** — retained for history but replaced by a newer version.

Never use a green visual style to imply scientific certainty merely because a page is technically published.

## Free-plan learner experience

The free campus can provide:
- searchable lesson content
- course/module indexes
- sequential previous/next navigation
- evidence cards
- study-path navigation
- self-check questions with collapsible answer explanations
- printable/copyable progress checklist
- capstone instructions and rubric
- certificate eligibility explanation

It cannot honestly provide, without a later compatible backend/LMS:
- secure individual accounts for course progress
- server-side saved lesson completion
- automated graded quizzes
- verified learner identity
- automatically issued credentials
- private Atlas storage

## Progress fallback at $0

Until a privacy-safe LMS/backend exists:

1. Offer a course checklist page that learners may print, copy into notes, or download from a repository/public file.
2. Let each lesson include a stable lesson ID and completion box in the checklist.
3. Do not store a learner's completion history in public WordPress comments or forms.
4. If a learner later requests a Certificate of Completion, use a documented manual evidence/portfolio workflow only after credential governance is approved.

## Assessment fallback at $0

Use native content rather than fake LMS grading:
- knowledge-check questions in the lesson
- Details blocks containing answer explanations/rationales
- homework prompts
- self-scoring rubric where appropriate
- instructor answer-key material only where publication policy permits

Do not present an unverified self-check as a clinical or psychometric test.

## Certificate boundary

The free public campus may explain the requirements for a future **Certificate of Completion** or **Certificate in HOSI Studies**, but it must not auto-issue or imply accreditation.

Before actual issuance, HOSI must have:
- credential policy
- identity/learner verification appropriate to the credential
- completion evidence
- assessment process
- issuance/revocation record
- privacy and retention rules

## Atlas boundary

The public WordPress campus may explain and link to the Atlas project, but it must not collect private Atlas reflections through ordinary public pages/comments/forms while the privacy-safe Atlas backend is not production-ready.

## Upgrade decision

Upgrade WordPress only after a concrete requirement is blocked by Free.

Examples:
- plugin-based LMS
- authenticated progress
- advanced assessment/grading
- automated certificates
- custom primary domain
- specialized integrations

Document the requirement and compare the cheapest compatible option at that future date. Do not pre-buy complexity because humans find dashboards reassuring.

## Files in this package

- `SITE_MANIFEST.json` — canonical campus route/content manifest
- `LESSON_TEMPLATE.md` — accessible public lesson template
- `BLOCK_PATTERNS.md` — native WordPress block recipes
- `PROGRESS_ASSESSMENT_CERTIFICATES.md` — honest free-plan workflows and upgrade gates
- `ACCESSIBILITY_CHECKLIST.md` — pre-publication accessibility review
- `PUBLISHING_WORKFLOW.md` — GitHub-to-WordPress status/release process

This package is a deployable content/IA blueprint, not evidence that a WordPress.com site has already been created or published.
