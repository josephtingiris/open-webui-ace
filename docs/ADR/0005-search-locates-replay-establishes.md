# ADR-0005: Search locates; replay establishes evidence

**Status:** Accepted

## Context

A search hit is only a clue. Similarity or textual match does not by itself establish the full remembered event.

## Decision

We will use search to return candidate coordinates and replay/exact retrieval to return source evidence.

## Consequences

Future lexical, semantic, or hybrid search can remain fuzzy while exact evidence stays deterministic.
