# ADR-0002: Scope current-chat retrieval from trusted context

**Status:** Accepted

## Context

A model-supplied chat identifier would mix navigation with authorization and could accidentally expand retrieval scope.

## Decision

We will scope normal retrieval from Open WebUI-injected current-chat context and use the host access-control boundary.

## Consequences

Current-chat retrieval does not require the model to choose its authority coordinate. Cross-chat retrieval requires a separate design.
