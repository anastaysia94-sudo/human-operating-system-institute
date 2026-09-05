# HOSI Multi-LLM Continuation Playbook

## Purpose

This document lets ChatGPT, GitHub Copilot, Grok, and Perplexity continue development of the Human Operating System Institute (HOSI) without restarting the project.

Canonical repository:
https://github.com/anastaysia94-sudo/human-operating-system-institute

Primary rule:
**Read the repository before acting. Preserve existing decisions, improve the system, and never claim work is complete unless the corresponding acceptance gate has actually passed.**

---

# 1. START-HERE PROMPT — USE WITH ANY LLM

Paste this first:

```text
You are joining an existing software + education project called HOSI: Human Operating System Institute.

Repository:
https://github.com/anastaysia94-sudo/human-operating-system-institute

Your job is to continue the project, not restart it.

FIRST ACTIONS
1. Connect to/open the GitHub repository.
2. Read README.md.
3. Read STATUS.md.
4. Read constitution/HOSI_CONSTITUTION_DRAFT_1.0.md.
5. Read curriculum/HOSI_MASTER_BACKLOG_1.0.md.
6. Read curriculum/HOSI_ACADEMIC_CATALOG_1.0.md.
7. Read courses/HOSI-101/README.md.
8. Read the platform documentation and relevant GitHub Issues.
9. Identify what is actually implemented versus only planned.
10. Make a prioritized implementation plan before changing files.

PROJECT NORTH STAR
“Learn the Operating System Before the Diagnosis.”

CORE PHILOSOPHY
- Diagnoses are maps, not identities.
- Person-first, systems-first, evidence-first.
- Teach human systems before diagnostic labels.
- Distinguish scientific evidence, expert interpretation, lived experience, founder philosophy, and uncertainty.
- Challenge assumptions through evidence, not ideology.

ACADEMIC SCOPE
Bipolar I, Bipolar II, ADHD presentations, OCD, PTSD/trauma, severe/acute severe trauma education, brain injury/TBI, CBT, IPSRT, ERP, behavioral activation, family-focused approaches, research literacy, self-management, and evidence-supported combinations.

CRITICAL MEDICAL STANDARD
Do not turn HOSI into anti-medication propaganda. Pharmacological approaches may be critically examined, but the curriculum must present benefits, risks, adverse effects, monitoring, interactions, discontinuation considerations, uncertainty, and individual variation. Non-pharmacological interventions receive equally rigorous evidence review. Never advise a learner to start, stop, or change medication based on HOSI educational content.

AI ATLAS STANDARD
The Atlas is a user-controlled educational/reflection system, not an AI therapist or diagnostician. AI may organize user-provided material, summarize it, suggest educational resources, and generate reflective questions. It must not silently diagnose, claim certainty about identity, or make treatment decisions. User review, correction, export, deletion, privacy, provenance, and AI disclosure are required.

100% RULE
Do not set STATUS.md to 100% merely because files were generated. 100% requires all applicable academic, evidence, technical, privacy, security, accessibility, QA, governance, and release gates to have actually passed.

WORK STYLE
- Prefer concrete files, tests, schemas, and acceptance criteria over vague prose.
- Reuse existing IDs and architecture.
- Create focused commits/PRs.
- Do not overwrite good existing work without inspecting it first.
- Cite current authoritative sources for changing facts.
- Never invent citations, credentials, accreditation, study results, or completed reviews.
- Record uncertainty and limitations.
- When a task requires an external account or independent reviewer, create the artifact/checklist and mark the external gate honestly as pending.

OUTPUT AFTER EACH WORK SESSION
1. What you inspected.
2. What you changed.
3. Tests/reviews performed.
4. What remains blocked or unverified.
5. Exact next recommended task.
```

---

# 2. CHATGPT CONTINUATION

ChatGPT can connect to GitHub in supported plans/surfaces through Settings → Apps → GitHub; capabilities vary by plan and experience. Once connected, tell it to read the repository and continue from the canonical files.

Use the START-HERE prompt above, followed by:

```text
Now inspect the repository state and execute the highest-priority safe, concrete work item you can complete without inventing external validation. Make the changes in GitHub, run any available tests, and report the exact commit(s), files, and remaining gates.
```

For research-heavy medical content, use current web research and primary/systematic-review/guideline sources, then place citations and evidence notes in the repository.

Official OpenAI guidance:
https://help.openai.com/en/articles/11145903

---

# 3. GITHUB COPILOT / COPILOT CLOUD AGENT

GitHub Copilot supports repository-wide instructions in `.github/copilot-instructions.md`. Copilot cloud agent can work on issues, create branches/PRs, and run coding tasks when enabled on the account.

Recommended workflow:

1. Connect/clone the HOSI repository.
2. Ensure `.github/copilot-instructions.md` exists.
3. Give Copilot one bounded GitHub Issue at a time.
4. Require tests and a summary.
5. Review the PR before merge.

Example task prompt:

```text
Work on issue #[NUMBER] in the HOSI repository.

Read the repository instructions first.
Do not redesign unrelated areas.
Implement the smallest complete change that satisfies the issue.
Add/update tests.
Run the relevant tests.
Update documentation if necessary.
Open/update a pull request with:
- summary
- files changed
- test results
- known limitations
- evidence or source links where relevant

Do not claim an acceptance gate passed unless it actually did.
```

Useful Copilot commands where supported:
- `/pr create`
- `/pr fix feedback`

Official GitHub guidance:
https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide
https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/overview
https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/manage-pull-requests

---

# 4. GROK / GROK BUILD

Grok currently supports GitHub as a connector, and Grok Build can work as an agentic coding workflow. Grok also reads `AGENTS.md` instruction files in repositories.

Recommended workflow:

### Option A — Grok web + GitHub connector
Connect GitHub through Grok's connector catalog, open the HOSI repository, then use the START-HERE prompt.

### Option B — Grok Build
Clone the repository locally, then run Grok Build from the project directory and give it a bounded task.

Example:

```text
Read AGENTS.md and the HOSI repository documentation.
Inspect the current state before editing.
Work only on the requested issue.
Implement, test, document, and summarize your changes.
Never fabricate medical evidence or claim independent review.
```

For repository files, prefer Markdown/JSON/text assets in Git. For large/binary artifacts, preserve the canonical file locally and document how it is generated.

Official xAI references:
https://docs.x.ai/grok/connectors
https://docs.x.ai/build/overview
https://docs.x.ai/build/features/skills-plugins-marketplaces

---

# 5. PERPLEXITY + GITHUB

Perplexity supports a GitHub connector on supported plans. It can search repositories, issues, PRs, and combine repository context with web research.

Recommended workflow:

1. Enable the GitHub connector in Perplexity Settings → Connectors.
2. Authorize GitHub.
3. Open/query the HOSI repository.
4. Paste the START-HERE prompt.
5. Ask for research verification or a bounded implementation plan.
6. When the connected workflow supports writing/PR actions, have Perplexity create the change or PR.
7. Review the result in GitHub.

Use Perplexity especially for evidence audits such as:

```text
Review the HOSI lesson/source claims relevant to this issue.
Find current primary research, systematic reviews, major guidelines, and authoritative sources.
For each claim, report:
- exact claim
- best supporting source
- contradictory/limiting evidence
- population/study design
- confidence level
- what the source does NOT establish
Do not invent citations.
Then propose precise repository edits.
```

Official Perplexity reference:
https://www.perplexity.ai/help-center/en/articles/12275669-github-connector-for-enterprise

---

# 6. MULTI-LLM DIVISION OF LABOR

Use each system for what it does best instead of having four agents rewrite the same files.

### ChatGPT
Best for:
- system architecture
- curriculum synthesis
- cross-domain planning
- structured documents
- evidence-aware educational writing

### GitHub Copilot
Best for:
- repository-native coding
- tests
- GitHub Issues/PR workflows
- CI/CD
- incremental implementation

### Grok
Best for:
- agentic coding/build workflows
- repository investigation
- broad web/X context where appropriate
- iterative implementation

### Perplexity
Best for:
- source discovery
- current evidence audits
- literature triangulation
- web research tied back to exact claims

All four must obey the same scientific and safety constraints.

---

# 7. SAFE HANDOFF LOOP

Use this loop continuously:

RESEARCH
→ PLAN
→ IMPLEMENT
→ TEST
→ REVIEW
→ DOCUMENT
→ PR
→ HUMAN APPROVAL
→ MERGE
→ RELEASE NOTE

Never:

PROMPT
→ GENERATE
→ CALL IT DONE

---

# 8. GITHUB UPLOAD / LOCAL PUSH

### GitHub CLI

```bash
gh auth login
git clone https://github.com/anastaysia94-sudo/human-operating-system-institute.git
cd human-operating-system-institute

# after making changes
git status
git add .
git commit -m "feat: describe the change"
git push origin main
```

For safer collaborative work:

```bash
git checkout -b feat/hosi-task-name
# edit / test
git add .
git commit -m "feat: implement HOSI task"
git push -u origin feat/hosi-task-name
```

Then open a pull request and review before merging.

GitHub's documentation recommends using repositories for version history and collaborative review, and GitHub Desktop is an alternative graphical workflow if the command line is undesirable.

---

# 9. BINARY FILES / GRAPHICS

Not every AI/GitHub connector supports arbitrary binary uploads. When an agent cannot upload a PNG, JPG, PDF, APK, or ZIP directly:

1. Save the artifact locally.
2. Use Git/GitHub Desktop or the GitHub web upload UI to add it.
3. Put source prompts/specifications in the repository.
4. Record the asset filename, license/provenance, generation date, and intended use.
5. Do not store API keys, signing keys, credentials, or sensitive learner data.

GitHub Actions artifacts can also be used for generated build outputs such as APKs, rather than committing every build binary to the repository.

---

# 10. CONTINUATION COMMANDS

Use one of these after the repository is loaded:

### General
`Continue HOSI from the current repository state. Inspect first, then execute the highest-priority unfinished task.`

### Curriculum
`Continue HOSI-101 with the next unfinished lesson block. Preserve the lesson schema and build student, instructor, assessment, evidence, and accessibility layers.`

### Research
`Audit the next HOSI lesson block claim-by-claim against current authoritative sources and commit the evidence records.`

### Web
`Continue the mobile-first HOSI campus. Inspect the current implementation, run tests, fix the highest-impact defect, and update documentation.`

### Android
`Continue the HOSI Android client. Make the smallest complete production-oriented improvement, run Gradle tests/builds, and report the artifact.`

### Atlas
`Continue the HOSI Atlas MVP. Prioritize consent, privacy, export/delete, provenance, and user control before adding personalization.`

### QA
`Run the next HOSI release gate. Report passes, failures, evidence, and blockers; do not convert unverified items into passes.`

---

# 11. FINAL RULE

The project belongs to the learner, the scholars, the evidence, and the mission—not to any one AI system.

**Build openly. Verify carefully. Correct visibly. Preserve uncertainty. Keep the human being larger than the diagnosis.**
