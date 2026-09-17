# HOSI Atlas backup, deletion, and retention policy — implementation draft

Status: **engineering policy for the synthetic/private-backend stage; human privacy/security review required before production.**

## Plain-language rule

When a person deletes Atlas data, the live application must stop using that data. The product must not claim deletion is complete while active summaries, graph links, search copies, or downloadable exports still contain the deleted narrative.

## Live-system deletion

The synthetic backend currently demonstrates these rules:

1. deleting an entry removes the primary entry;
2. foreign-key deletion removes AI summaries and graph edges that depend on it;
3. stored export snapshots for that Atlas are deleted;
4. consent scopes are rewritten so the deleted entry cannot remain authorized for future processing;
5. account deletion removes author-owned Atlas, entry, consent, derived-data, export, and session records;
6. a minimal deletion tombstone may remain with opaque user ID, timestamp, and record counts, but no email or narrative.

## Production backup boundary

Production backup infrastructure is not implemented yet. Before real sensitive data is allowed, the production design must document and test:

- backup encryption at rest and in transit;
- who can restore backups;
- a maximum backup-retention window;
- how deleted records age out of backups;
- how emergency restores avoid silently resurrecting deleted live records;
- restore drills using synthetic data;
- destruction/expiry evidence for obsolete backups.

A reasonable future target is the shortest retention window compatible with reliable recovery and legal obligations. The exact duration must be chosen only after human privacy/security/legal review; this repository does not invent one.

## User-held exports

An export already downloaded by the author cannot be remotely erased by HOSI. The interface must explain that distinction. Copies still retained by HOSI remain subject to the disclosed deletion/retention policy.

## No fake completion

A UI disappearing is not proof of deletion. A backup existing is not proof that restore works. Both deletion and restore behavior require end-to-end production tests before release.
