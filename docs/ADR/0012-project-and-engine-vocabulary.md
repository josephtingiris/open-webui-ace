# ADR-0012: Project and Engine Vocabulary

Status: Accepted

## Context

Early project language treated ACE as the proper name of one Open WebUI tool. The work now distinguishes a broader project from individual host-specific engines and anticipates additional implementations.

## Decision

Use the following vocabulary:

- `ACE`: the project exploring Agent Continuity Engines;
- `an ACE`: one Agent Continuity Engine;
- `the Open WebUI ACE`: the implementation in this repository;
- `ACEs`: multiple engines or implementations.

The public front door leads with value:

```text
Extend your context. Enhance your capabilities. Economically.
```

The Open WebUI implementation is then described concretely:

```text
Open WebUI already saves your conversations. The Open WebUI ACE lets
agents quickly find and replay earlier messages into their current
context window.
```

## Consequences

Project language can grow beyond one host without claiming that all platforms retain the same records or provide the same access boundaries.

README prose should use `the ACE` or `an ACE` when referring to an engine. Bare `ACE` refers to the project unless a code identifier or established contract requires otherwise.
