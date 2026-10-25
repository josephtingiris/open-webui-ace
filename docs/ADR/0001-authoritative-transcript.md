# ADR-0001: Persisted transcript is authoritative

**Status:** Accepted

## Context

ACE needs a stable source for what actually occurred. Summaries, embeddings, indexes, and recollections can omit or transform the path.

## Decision

We will treat the persisted Open WebUI transcript as authoritative evidence for chat events. Derived structures remain navigation aids.

## Consequences

Search and semantic layers must remain traceable to exact persisted messages. Unresolved evidence is preferable to invented history.
