# ADR-0007: Prefer platform-native and standard-library mechanisms first

**Status:** Accepted

## Context

ACE can begin with Open WebUI application interfaces and Python stdlib. Premature infrastructure would add operational complexity before requirements are measured.

## Decision

We will add dependencies only when observed retrieval quality, scale, or operations justify them.

## Consequences

PostgreSQL, pgvector, embeddings, and relational indexing remain available future options rather than initial commitments.
