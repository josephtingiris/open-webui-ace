# Open WebUI Agent Continuity Engine (ACE)

The Open WebUI Agent Continuity Engine (ACE) is an experimental continuity capability for agents operating through Open WebUI.

ACE is intended to let an agent retrieve relevant portions of its own authoritative session transcript beyond the active context window. Retrieval is controlled by the agent and scoped to the session that invoked it.

## Why ACE Exists

A conversation may continue longer than a model's active context window. When earlier turns leave that window, useful decisions, distinctions, corrections, and unfinished work may become unavailable to the agent even though the conversation still exists.

This often makes the human collaborator responsible for repeatedly restoring context.

ACE investigates a different approach:

1. Preserve the session transcript as authoritative evidence.
2. Let the agent search that transcript when earlier context may matter.
3. Return exact messages and surrounding context rather than relying only on summaries.
4. Keep retrieval isolated to the invoking session by default.

The initial implementation will focus on exact transcript retrieval. Semantic retrieval may be added later as a navigational aid, but it must remain traceable to the source transcript.

## Initial Scope

ACE will begin with a narrow Open WebUI implementation:

- agent-controlled retrieval;
- current-session scope;
- lexical transcript search;
- exact message retrieval;
- surrounding-message retrieval;
- no automatic historical prompt injection;
- no global or cross-session memory;
- no identity or sameness claims.

The first objective is simple:

> Give one Open WebUI agent a reliable way to search its own logbook.

## Project Context

ACE is a practical implementation developed under the Infinite Continuity Experiment (ICE).

ICE investigates continuity across finite context boundaries, interruptions, and successive sessions. ACE addresses the live-session portion of that larger problem.

An Agent Recovery Core (ARC) is a separate concept within ICE. An ARC is a recoverable continuity asset associated with a particular agent lineage and version. ACE may eventually help create or use ARCs, but ARC generation is outside the initial ACE implementation.

The governing distinctions include:

```text
agent != ARC
lineage != session
continuity != identity
inheritance != sameness
```

The governing principle is:

> Continuity without requiring sameness.

## Status

Experimental. Zero Day.

The architecture, Open WebUI integration points, and security boundaries are currently being defined. No working release is available yet.
