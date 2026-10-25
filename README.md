# Extend your context. Enhance your capabilities. Economically.

**ACE is a project exploring Agent Continuity Engines.**

Open WebUI already saves your conversations. **The Open WebUI ACE lets your agents quickly find and replay earlier messages into their current context window.**

## Extend your context

A conversation can grow beyond a model's active context window while its earlier messages remain saved in Open WebUI.

The Open WebUI ACE gives an agent a way to look back for itself. It can find an earlier message, resolve a compact historical coordinate, and replay the exact message or its surrounding conversation into current context.

```text
find
-> resolve
-> replay
-> continue
```

## Enhance your capabilities

More context is valuable because of what an agent can do with it.

The Open WebUI ACE can help an agent:

- recover earlier decisions, distinctions, and corrections;
- resume unfinished work;
- revisit the conversation around a prior choice;
- check the saved record instead of plausibly reconstructing it;
- keep working with less repeated explanation from its human collaborator.

The current implementation begins with saved messages. The larger ACE project is exploring how Agent Continuity Engines may navigate additional recorded history, including reasoning traces, actions, results, and artifacts, without confusing those sources with derived summaries or indexes.

## Economically

**More continuity. Less catch-up.**

Selective replay avoids requiring the entire conversation to occupy the active context window on every turn. The human repeats less, the agent retrieves bounded history when needed, and current work can proceed without carrying everything that came before.

This is an architectural objective, not yet a universal cost benchmark. ACE will earn stronger economic claims through measurement of retrieval latency, context introduced, successful resolution, repeated explanation avoided, and the operating cost of any derived indexes.

## Current Release

The Open WebUI ACE 0.3.1 is the current Zero Day implementation. It provides:

- agent-controlled retrieval from the current Open WebUI conversation;
- lexical and temporal find;
- exact message replay;
- surrounding-message replay;
- canonical historical turns;
- compact `~N` navigation coordinates;
- source-time projection into the navigator's timezone;
- oldest-first or newest-first independent find presentation;
- initial trajectory-integrity findings;
- explicit unresolved results;
- no automatic historical prompt injection;
- no cross-conversation retrieval by default;
- no identity or sameness claims.

## Canonical Historical Turn

Historical turns use one visible grammar:

```text
~<where> · <when> · <who>:
<what>
```

Example:

```text
~60 · Oct 25, 9:13 AM EDT · you:
saved message content
```

- **where** is an ACE navigation coordinate;
- **when** is the recorded source instant shown in the navigator's timezone;
- **who** projects stored roles conversationally (`user -> you`, `assistant -> me`);
- **what** is the saved source content.

The coordinate is a bearing, not the source record itself. Open WebUI message IDs, topology, source timestamps, and other provenance remain below deck.

## Core Invariants

1. Open WebUI owns the saved conversation, schema, persistence, and access controls used by this implementation.
2. Saved source records remain distinct from the maps used to navigate them.
3. Normal retrieval scope comes from trusted Open WebUI-injected current-chat context.
4. Exact-message and replay paths preserve source content as exposed by Open WebUI.
5. Recorded source timestamps are never synthesized, interpolated, corrected, or used to reorder source topology.
6. Plausible reconstruction is not recovered history; unresolved is legitimate.
7. Derived indexes, summaries, excerpts, embeddings, and relationships are navigation aids, not replacements for sources.
8. Once durable lineage coordinates exist, assigned coordinates must never be rebound or reused.
9. Cross-conversation retrieval requires its own authorization boundary.
10. Continuity, recovery, inheritance, and retrieval do not establish identity or sameness.
11. Prefer simple deterministic machines and platform-native interfaces; add infrastructure only when measurement earns it.

## Project and Engine Vocabulary

- **ACE** is the project exploring Agent Continuity Engines.
- **An ACE** is one Agent Continuity Engine.
- **The Open WebUI ACE** is the implementation in this repository.
- **ACEs** are multiple engines or implementations across host platforms.

The Open WebUI ACE is developed under the Infinite Continuity Experiment (ICE). An Agent Recovery Core (ARC) is a separate recoverable continuity asset associated with an agent lineage and version.

```text
agent != ARC
lineage != session
continuity != identity
inheritance != sameness
```

> Continuity without requiring sameness.

## North Star

ACE builds infrastructure that lets a finite navigator participate in a history much larger than any active context.

The history may grow without requiring active context to grow with it.

## Documentation

- `README.md`: front door, current capability, project vocabulary, and shared invariants.
- `docs/ARCHITECTURE.md`: current architecture, boundaries, and extension direction.
- `docs/ADR/`: durable reasons for consequential decisions.
- `CHANGELOG.md`: versioned changes and unreleased documentation work.

## Status

Experimental. Zero Day. ACE 0.3.1 is under live qualification. Behavior not yet observed live should not be described as proven.
