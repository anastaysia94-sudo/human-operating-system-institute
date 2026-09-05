# HOSI Platform Architecture v1.0

## MVP principle
Build the smallest credible public campus first; keep curriculum content portable in Markdown/JSON so the project is not locked to one LMS.

## Layers
1. **Public campus** — WordPress.com or compatible WordPress host.
2. **Content source** — GitHub Markdown/JSON as canonical source for curriculum and policies.
3. **References** — Zotero or a structured bibliography.
4. **Learning layer** — LMS features for courses, quizzes, assignments, certificates when the chosen WordPress tier supports them.
5. **Atlas layer** — learner-controlled reflection/timeline data.
6. **AI layer** — retrieval-grounded educational assistant; no autonomous diagnosis.
7. **Quality layer** — versioning, source checks, accessibility checks, safety review.

## Mobile-first requirements
- Responsive typography and spacing
- Large tap targets
- Minimal horizontal scrolling
- Progressive disclosure for long lessons
- Downloadable text alternatives
- Captions/transcripts for audiovisual material
- Keyboard navigation
- Screen-reader semantics
- Low-bandwidth friendly pages

## Source of truth
GitHub source files are canonical for content drafts. WordPress is a publication surface, not the primary scholarly archive.

## Security principle
Do not place secrets, API keys, private health information, or credentials in the public repository.

## AI principle
AI may help organize and explain educational content. It must cite the underlying source set when making factual claims, disclose uncertainty, and defer clinical decisions to qualified professionals.
