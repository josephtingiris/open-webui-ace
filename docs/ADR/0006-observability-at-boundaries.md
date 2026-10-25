# ADR-0006: Observe continuity boundaries explicitly

**Status:** Accepted

## Context

ACE depends on artifact delivery, tool registration, model-visible schema, runtime code, trusted context, and persistence. These seams can drift independently.

## Decision

We will retain economical diagnostics for build identity, semantic contract, trusted scope, and retrieval state, and use versioned artifacts with digests for handoff.

## Consequences

Operational failures can be localized without injecting diagnostic noise into normal recall.
