# ADR-0011: Tilde Coordinate Notation Experiment

Status: Accepted for qualification

## Context

ACE 0.2 and 0.3.0 used `@N` as a compact current-trajectory coordinate. Live use showed that the compact numeric reference is valuable, but `@` is heavily occupied by chat mention semantics and by Open WebUI's input surface. ACE is still early enough that notation should follow observed ergonomics rather than accidental permanence.

Tilde already carries conventional navigation and relationship semantics: in shells it resolves compact contextual notation such as home and directory-stack positions; elsewhere it commonly signals relation, similarity, or approximation. Those meanings align with ACE's split between stochastic recollection, compact bearings, deterministic resolution, and exact persisted evidence.

## Decision

ACE 0.3.1 changes the experimental visible coordinate spelling from:

```text
@20
```

to:

```text
~20
```

The coordinate's current implementation remains trajectory-position based and the runtime contract remains `trajectory-v1`. This ADR does not claim durable lineage-coordinate persistence.

`~N` is a coordinate only in an ACE navigation context. Occurrences of tilde notation inside persisted evidence remain sacred content and must never be reinterpreted or mutated merely because they resemble ACE notation.

## Consequences

ACE will qualify `~N` through live human and agent use before promoting the notation to a stronger invariant.

The change intentionally creates a small compatibility break during Zero Day. Bare decimal coordinate input remains accepted by the resolver during this experiment; old `@N` notation is not advertised by 0.3.1.
