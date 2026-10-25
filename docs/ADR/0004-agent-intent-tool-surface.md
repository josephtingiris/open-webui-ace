# ADR-0004: Name public tools by agent intent

**Status:** Accepted

## Context

The model chooses tools from names, descriptions, and parameter guidance. Implementation-shaped names expose mechanism instead of purpose.

## Decision

We will use the `ace_<action>_<object>` public naming grammar and keep implementation helpers private.

## Consequences

Storage and ranking implementations can evolve while the agent-facing vocabulary remains coherent.
