# HOSI Atlas MVP — UX Flow

## UX principle

The author should always be able to answer three questions:

1. **What is stored?**
2. **Who can see or process it?**
3. **How do I change, export, or delete it?**

Privacy controls must be understandable without reading a legal document.

## Flow A — Create Atlas

### Screen 1: What the Atlas is
Show:
- reflective/learning archive
- author ownership
- private by default
- not a diagnosis or clinical evaluation
- sensitive information is optional

Primary action: **Create private Atlas**
Secondary action: **Continue HOSI without an Atlas**

### Screen 2: Choose Atlas type
- Founder
- Learner
- Visitor/minimal profile

Explain that type changes templates, not ownership rights.

### Screen 3: Base privacy
Default:
- visibility: private
- AI processing: off until purpose-specific consent
- research use: off
- public sharing: off

## Flow B — Create a reflection

1. Select prompt or blank reflection.
2. Show optional “Skip this question” action.
3. Write/save locally in editor state.
4. Before save, allow sensitivity label.
5. Save as private by default.
6. Record provenance event.

Sensitive prompt categories should display:
> You do not need to disclose personal history to complete HOSI coursework. You may skip, generalize, or use a fictional/example response.

## Flow C — Founder oral-history question

Question card includes:
- question ID
- prompt
- why HOSI is asking
- reflection guidance
- “skip / answer later”
- timeline/context
- memory confidence
- corroboration (optional)
- alternative interpretations
- Cornell Notes
- lessons learned
- future reflection

Memory confidence UI text:
> This records how certain the memory feels to you. It does not measure whether the event is factually verified.

## Flow D — AI summary

### Step 1: Select source entries
User explicitly selects entries or an approved category.

### Step 2: Consent preview
Show:
- selected entries/categories
- purpose
- whether output will be stored
- AI disclosure
- withdrawal/delete controls

### Step 3: Generate
Result state = `user_review_required`.

The AI panel must visually separate:
- author-written source
- AI summary
- inferred themes
- uncertainty note

### Step 4: Author decision
Buttons:
- Accept
- Edit then accept
- Reject
- Delete summary

Rejecting does not alter source entries.

Accepted text still retains AI provenance.

## Flow E — Suggested reflection question

Atlas AI may suggest a question such as:
> You mentioned that routines helped during several periods. Would you like to reflect on what made those routines easier to maintain?

It must not convert this into:
> Your pattern proves you have condition X.

User controls:
- answer
- dismiss
- do not suggest this topic again

## Flow F — Timeline

Timeline can display:
- author-created events
- uncertain dates
- date ranges
- corroboration status
- accepted AI-organized groupings

Never visually present `uncorroborated_recollection` as identical to independently corroborated fact.

## Flow G — Knowledge graph

Nodes may include:
- reflections
- goals
- values
- projects
- lessons
- research claims
- timeline events

Edges must identify provenance:
- user-created
- imported
- AI-suggested / pending approval
- AI-suggested / accepted

No hidden diagnosis node.

## Flow H — Privacy dashboard

Show a simple inventory:

### Visibility
- private entries count
- selected-sharing count
- public count

### AI
- AI consent status
- entries eligible for processing
- stored AI summaries
- rejected summaries still retained, if any

### Research
- research-use consent: on/off
- plain-language description of any active research consent

### Devices / sessions
- active sessions when supported
- sign out other sessions

### Data controls
- export
- delete selected content
- delete Atlas

## Flow I — Share

1. Choose exact entry/collection.
2. Choose audience.
3. Preview content and audience.
4. If public, show explicit warning.
5. Confirm.
6. Record provenance.

Never combine “save” and “publish” into one ambiguous button.

## Flow J — Export

1. Request export.
2. Show included categories.
3. Re-authenticate when appropriate.
4. Prepare archive.
5. Offer short-lived authenticated download.
6. Record completion and expiration.

Export should include human-readable and machine-readable representations where practical.

## Flow K — Delete one entry

1. User chooses Delete.
2. Show what derived items are affected, such as AI summaries or graph edges.
3. Confirm.
4. Mark deletion state and run deletion orchestration.
5. Report success/failure honestly.

## Flow L — Delete entire Atlas

1. Explain scope.
2. Offer export first, without making export mandatory.
3. Require deliberate confirmation.
4. Re-authenticate when appropriate.
5. Begin deletion state machine.
6. Provide status.
7. Do not call deletion complete until active data and documented derived stores are processed.

## Flow M — Withdraw AI consent

1. Turn off AI processing for future use.
2. Explain effect on existing summaries.
3. Offer deletion of stored derived summaries.
4. Enforce withdrawal before another AI request is allowed.

## Flow N — Correct a record

The author may:
- edit original reflection
- add a correction note
- update corroboration status
- reject/correct an AI summary

Provenance should preserve who made the change and when without unnecessarily preserving deleted sensitive content.

## Accessibility requirements

- keyboard-operable privacy controls
- screen-reader labels for visibility and AI state
- no color-only privacy indicators
- plain-language consent
- no countdown pressure for sensitive decisions
- save/skip options for cognitively demanding prompts
- predictable headings/navigation
- reduced-motion support where motion is used
- sufficient touch targets on mobile

## Content-safety UX

Atlas is not crisis monitoring by default and must not secretly classify reflections into clinical-risk scores.

If HOSI later offers explicit safety features, their purpose, limits, data use, escalation path, false-positive/false-negative risk, and consent model require a separate reviewed design.
