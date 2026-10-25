# ACE Architecture

## Purpose

The Open WebUI Agent Continuity Engine (ACE) lets an agent locate and replay exact evidence from its persisted current-chat trajectory when relevant history is no longer confidently present in active context.

This document describes the architecture as it exists now. `docs/ADR/` records why consequential decisions were made.

## North Star

```text
agent reasoning
    stochastic, interpretive, selective
            |
            v
ACE quarterdeck
    semantic tool surface
    economical search and replay
            |
            v
ACE engine room
    trusted coordinates
    access control
    branch reconstruction
    provenance
    diagnostics
            |
            v
Open WebUI persisted chat
    authoritative transcript evidence
```

> Preserve richly below deck. Surface minimally above deck.

The agent should experience continuity, not database administration.

## Proven Flow

ACE has demonstrated this live path:

```text
natural continuity intent
    -> lexical search
    -> compact candidate coordinate
    -> bounded exact replay
    -> agent interpretation
    -> optional next cue / traversal
```

The first live participant, Moss, used this path autonomously during ACE 0.2.0 testing.

## Evidence and Navigation

The persisted Open WebUI transcript is authoritative for what occurred in the chat. Derived structures help navigate; they do not become the past.

```text
search   -> where should I look?
replay   -> what actually happened here?
reason   -> what might this evidence mean?
```

The distinction permits future fuzzy navigation without fuzzy evidence.

## Trusted Scope

Normal retrieval begins with Open WebUI-injected current-chat context and passes through Open WebUI's access-controlled chat interface. The model does not supply the authoritative current-chat coordinate.

Cross-chat retrieval requires an explicit future authorization design.

## Public Tool Surface

Public methods use `ace_<action>_<object>` and describe agent intentions. Private helpers describe implementation mechanisms.

Current surface:

```text
ace_check_context
ace_get_chat
ace_search_transcript
ace_get_message
ace_get_context
```

The tool descriptions themselves are behavioral architecture: they teach when recall should use ACE rather than guessing or generic web retrieval.

## Coordinates

Durable Open WebUI message IDs remain below deck. ACE 0.2.0 introduced compact local handles such as `@13` for normal navigation.

A local handle is intentionally lightweight and must not silently be treated as durable across branch mutation.

## Economical Recall

Search returns compact clues. Replay restores a small exact neighborhood. The normal interface avoids UUIDs, parent links, timestamps, and structural JSON unless those details are requested for diagnostics or provenance.

This allows the present to remain small while extending what it can reach.

## Replay Fidelity

Normal replay projects storage roles into conversational labels:

```text
user      -> you
assistant -> me
```

The labels are navigation aids. The underlying persisted role remains unchanged.

Message content is evidence and must not be rewritten by ACE on exact retrieval or replay paths. Search previews may normalize text because they are derived clues.

ACE 0.2.0 exposed a fidelity defect: exact-message and replay paths strip leading/trailing whitespace. The 0.2.x line should correct it without changing the retrieval model.

## Retrieval as Traversal

A recovered coordinate can become a place from which the agent notices another cue:

```text
locate
    -> replay
    -> reason
    -> notice a related cue
    -> locate again
    -> re-center
```

This suggests future semantic and relational navigation. It does not yet justify a vector or graph implementation. Lexical search remains the current deterministic locator.

## Deterministic Footing, Stochastic Reasoning

ACE does not make thought deterministic. It makes selected footing deterministic where practical:

```text
which build ran
which chat was bound
which coordinate was recovered
which persisted content exists there
which retrieval method produced a candidate
whether retrieval succeeded or remained unresolved
```

> Deterministic footing for fluid thought.

## Observability

Operational seams are first-class:

```text
artifact delivery
    version + digest

repository
    revision + history

Open WebUI registration
    visible integration metadata

model semantic surface
    tool names + docstrings + parameter descriptions

runtime
    ACE version + semantic contract + trusted context

retrieval
    source + method + resolved/unresolved state
```

The 0.2.0 installation exercise demonstrated why these layers must not be assumed identical.

## Dependency Strategy

Start with Python stdlib and Open WebUI application interfaces. Add infrastructure when measurement earns it.

Possible future layers include full-text indexes, PostgreSQL, pgvector, embeddings, relational indexes, and distributed retrieval.

## Scale

ICE may try to preserve and retrieve as much earned history as practical for as long as practical. ACE does not assume forgetting is required. Active context can remain finite while reachable history grows.

> Keep the present small while extending what the present can reach.

## Security

Workspace Tools possess substantial server-side capability. ACE should exercise less privilege than the host technically permits. Current-chat retrieval is scoped from trusted injected context and uses Open WebUI's access-control boundary. Authentication material and broad request/user objects must not be returned through normal tools.

## Decision Records

Consequential decisions are maintained under `docs/ADR/`:

```text
0001 authoritative transcript
0002 trusted current-chat scope
0003 quarterdeck / engine-room separation
0004 agent-intent public tool surface
0005 search locates; replay establishes evidence
0006 observability at boundaries
0007 platform-native and stdlib first
0008 pristine evidence replay
```

When a decision changes, preserve the record and supersede it with a new ADR.

## Near-Term Work

1. Correct replay fidelity in 0.2.x.
2. Make version identity easier to inspect operationally.
3. Test longer-lived agents and histories.
4. Measure replay-window cost and usefulness.
5. Observe iterative retracing before choosing semantic or relational indexing.
