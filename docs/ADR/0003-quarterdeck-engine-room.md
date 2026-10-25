# ADR-0003: Separate quarterdeck from engine room

**Status:** Accepted

## Context

Rich structural metadata is useful for machinery and provenance but expensive and distracting in normal reasoning.

## Decision

We will preserve rich structure below deck and surface only the minimal navigation and evidence needed above deck.

## Consequences

UUIDs, parent links, timestamps, topology, and diagnostic details remain available without burdening ordinary recall.
