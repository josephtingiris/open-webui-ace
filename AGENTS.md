# Open WebUI Agent Continuity Engine (ACE)

## Purpose

This repository contains the Open WebUI Agent Continuity Engine (ACE).

ACE is intended to provide agent-controlled, session-scoped retrieval from an authoritative Open WebUI session transcript beyond the model's active context window.

## Current Development Phase

The project is in the definition phase.

Do not present planned behavior as implemented behavior. Clearly distinguish:

```text
observed behavior
documented platform behavior
design decisions
working hypotheses
future possibilities
```

## Core Invariants

Preserve these invariants in every design and implementation proposal:

1. The persisted session transcript is authoritative evidence.
2. Retrieval is scoped to the invoking session by default.
3. Normal retrieval scope must come from trusted request context.
4. Do not trust a model-supplied session or chat identifier as the authority for normal retrieval scope.
5. The agent decides when historical retrieval is necessary.
6. Do not inject historical material automatically unless a later approved design explicitly requires it.
7. Search indexes, embeddings, summaries, and caches are derived aids, not replacements for the transcript.
8. Semantic search results must remain traceable to exact source messages.
9. Cross-session retrieval requires an explicit, separately designed boundary.
10. Do not infer identity, sameness, memory, resurrection, or subjective continuity from transcript retrieval.

## Initial Implementation Boundary

The first implementation should support only:

```text
current session
exact lexical search
exact message retrieval
surrounding-message retrieval
compact navigational results
```

Do not add the following without an approved design change:

```text
global memory
cross-session retrieval
automatic prompt injection
ARC generation
lineage management
branch management
vector retrieval
summary generation
Git-backed runtime state
```

These may become later capabilities. They are not part of the first implementation merely because they are discussed elsewhere.

## Terminology

Define an acronym before using it in each independently readable document.

Use these terms consistently:

### Open WebUI Agent Continuity Engine (ACE)

The live continuity machinery being developed for Open WebUI.

### Infinite Continuity Experiment (ICE)

The umbrella experiment under which ACE is being developed.

### Agent Recovery Core (ARC)

A recoverable continuity asset associated with a particular agent lineage and version.

An ARC is not an agent.

### Authoritative transcript

The preserved, ordered session messages and their source metadata.

### Derived index

A regenerable lexical, semantic, or navigational structure produced from the authoritative transcript.

### Retrieval

Obtaining preserved historical material.

### Recovery

Restoring useful working context from preserved historical material.

### Inheritance

Allowing a later agent or lineage to use preserved material.

Retrieval, recovery, and inheritance do not establish identity or sameness.

## Provenance Requirements

Maintain traceability across every transformation:

```text
transcript or source evidence
    -> selected source material
    -> derived index or summary
    -> agent retrieval result
    -> receiving-agent use
```

When derived material is introduced, record enough information to identify:

```text
source
method
configuration
relevant dependencies
output
known limitations
```

Do not describe incomplete provenance as complete provenance.

Do not describe an ideal future state as current system behavior.

## Collaboration Protocol

For new durable assets and consequential changes:

```text
propose
    -> inspect
    -> agree
    -> commit
    -> observe
```

Show proposed content before creating or substantially changing a durable project asset.

Do not make speculative repository changes merely because they appear useful.

Prefer one meaningful change at a time.

## Source Hierarchy

When sources disagree, use this order:

1. The running system establishes observed behavior.
2. The repository establishes what was intentionally built.
3. The current design discussion establishes what is being considered.

Inspect discrepancies rather than silently reconciling them.

## Documentation Responsibilities

Use `README.md` for human-facing purpose, scope, status, and usage.

Use `AGENTS.md` for agent-facing invariants, terminology, workflow, and implementation constraints.

Avoid duplicating substantial prose between the two files.

If a concept requires one authoritative explanation for both audiences, propose a shared document before duplicating it.

## Security

Open WebUI Tools and Functions execute server-side code and may access sensitive application state.

Treat session isolation as a security boundary.

Do not:

- expose another session through accidental scope expansion;
- return authentication material;
- log full transcripts unnecessarily;
- place credentials in source code;
- add network transmission without explicit review;
- claim isolation until it has been tested against the running Open WebUI version.

## Working Standard

Build the smallest testable mechanism that preserves the approved invariants.

The first engineering question is:

> What trusted session-specific context does an Open WebUI Workspace Tool receive when the model calls it?

Do not design later retrieval layers until that boundary has been observed and documented.
