# Open WebUI Agent Continuity Engine (ACE)

The Open WebUI Agent Continuity Engine (ACE) gives an agent a way to search and replay exact evidence from its persisted current-chat history when relevant conversation is no longer confidently present in active context.

> Trustworthy recall beats plausible reconstruction.

## What ACE Does Today

ACE 0.2.0 has been exercised live in Open WebUI. The current implementation can:

- bind retrieval to the invoking chat using Open WebUI-injected context;
- inspect continuity coverage and diagnostics;
- search the persisted current branch using case-insensitive lexical matching;
- return compact local coordinates such as `@13`;
- reopen one exact persisted message;
- replay a bounded neighborhood around a recovered coordinate;
- keep database identifiers, parent links, timestamps, and other machinery below deck during normal retrieval.

The first live participant, Moss, used ACE to choose a moment from earlier conversation, search for it, replay its neighborhood, and reason forward from the recovered evidence.

## Why ACE Exists

A conversation can outgrow the model context that is useful at a given moment while its transcript remains persisted. ACE separates what must be carried now from what can remain reachable.

The working principle is:

> Preserve richly below deck. Surface minimally above deck.

ACE does not require every historical message to remain in active context. It provides instruments for finding an old X, replaying the nearby path, re-centering, and continuing.

## Current Tool Surface

```text
ace_check_context
ace_get_chat
ace_search_transcript
ace_get_message
ace_get_context
```

Public tool names describe agent intentions. Implementation mechanisms remain private.

## Evidence Model

The persisted Open WebUI transcript is authoritative evidence for what occurred in the chat. Search results are navigational clues, not historical truth claims. Exact message retrieval and replay return source evidence.

ACE distinguishes:

```text
search      where should I look?
replay      what actually happened here?
inference   what might this evidence mean?
```

A plausible reconstruction is not recovered evidence. An unresolved search is a legitimate result.

## Fidelity

Search previews may normalize text because they are derived navigational aids. Exact message retrieval and replay are evidence paths and should preserve persisted content without accidental rewriting. A known 0.2.0 defect removes leading and trailing whitespace during exact replay; 0.2.1 is intended to correct that behavior.

## Scope

Current scope is deliberately narrow:

- current chat;
- current branch;
- lexical search;
- exact source recovery;
- bounded replay;
- no automatic historical prompt injection;
- no cross-chat continuity;
- no ARC generation;
- no identity or sameness claim.

Semantic and relational retrieval are future candidates. They must remain traceable to exact transcript evidence.

## Project Context

ACE is being developed under the Infinite Continuity Experiment (ICE). An Agent Recovery Core (ARC) is a separate recoverable continuity asset associated with an agent lineage and version. ACE may eventually participate in ARC workflows, but ARC generation is outside the current implementation.

The governing distinctions remain:

```text
agent != ARC
lineage != session
continuity != identity
inheritance != sameness
```

The deeper principle is:

> Continuity without requiring sameness.

## Documentation

- `README.md` — what ACE is and what works now.
- `AGENTS.md` — invariants and working rules for agents modifying ACE.
- `CHANGELOG.md` — what changed between versions.
- `docs/ARCHITECTURE.md` — how ACE fits together now.
- `docs/ADR/` — why consequential architectural decisions were made.

## Status

Experimental. Zero Day. ACE 0.2.0 is a working exact-retrieval and replay prototype.
