# HOSI Atlas synthetic backend

This directory is the first executable implementation of the Atlas authorization/data-boundary contract.

## What it proves

The CI backend uses only Python's standard library and SQLite so privacy invariants can be tested without production credentials or real user data. It implements:

- account registration with salted `scrypt` password hashing;
- random sessions with only SHA-256 token hashes stored server-side;
- server-side owner checks for private Atlas objects;
- owner-scoped search;
- purpose-specific, entry-specific consent;
- AI-summary records that begin in `user_review_required` state;
- export restricted to the requesting author's Atlas;
- deletion cascading through primary and derived live records;
- minimal security audit events that omit narrative content.

## What it does **not** prove

This is a synthetic test backend, not the production Atlas service. A green CI run does not establish independent penetration testing, legal compliance, production encryption/key management, accessibility, clinical review, or safe handling of real sensitive narratives.

No real personal, medical, trauma, treatment, or learner data should be put into this test backend.

## Run locally

```bash
python scripts/test_atlas_backend.py
```

The test suite creates only fictional users under the reserved `.invalid` domain and destroys the in-memory database after each test.
