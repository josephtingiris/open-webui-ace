# Open WebUI Agent Continuity Engine (ACE)

## Purpose

This repository contains ACE, a session-scoped continuity capability for agents operating through Open WebUI.

Work from observed evidence. Do not present planned behavior as implemented behavior. Distinguish observed behavior, documented platform behavior, design decisions, working hypotheses, and future possibilities.

## Core Invariants

1. The persisted chat transcript is authoritative evidence for what occurred.
2. Normal retrieval scope comes from trusted Open WebUI-injected context.
3. Do not trust a model-supplied chat ID as the authority for normal current-chat retrieval.
4. Search indexes, embeddings, summaries, caches, and relationships are derived navigation aids, not replacements for transcript evidence.
5. Search locates. Exact retrieval and replay establish source evidence.
6. Plausible reconstruction is not recovered evidence.
7. Unresolved retrieval is a legitimate result.
8. Preserve richly below deck; surface minimally above deck.
9. Public tool methods name agent intentions; private helpers name mechanisms.
10. Retrieval, recovery, inheritance, and continuity do not establish identity or sameness.
11. Do not inject historical material automatically unless a later accepted design explicitly requires it.
12. Cross-chat retrieval requires a separately designed authorization boundary.

## Evidence Fidelity

Navigation may compress. Evidence does not.

Search excerpts may normalize whitespace because they are derived clues. Exact-message retrieval and replay must return the persisted message content without ACE rewriting it. Do not call `strip()`, `lstrip()`, `rstrip()`, collapse whitespace, normalize newlines, re-indent, clean Markdown, alter Unicode, or intentionally escape/unescape source content on evidence paths.

ACE can preserve only what Open WebUI exposes to it. Do not claim pristine origin beyond the persisted source content.

## Public API Grammar

Use:

```text
ace_<action>_<object>
```

Keep the verb set small and semantic:

```text
check   diagnostic or validation
get     retrieve a known object or state
list    enumerate
search  locate candidate coordinates
set     alter explicitly ACE-owned state
index   build or refresh derived retrieval state
```

Current public methods include:

```text
ace_check_context
ace_get_chat
ace_search_transcript
ace_get_message
ace_get_context
```

Helper methods must remain private with leading underscores.

## Tool Semantics

Names, docstrings, and parameter descriptions are part of the agent-facing interface. Spend this semantic surface carefully. Teach when and why to use continuity retrieval, not database mechanics.

Continuity intents include questions such as whether something is remembered, what was said earlier, what happened before, or requests to look back. Treat examples as semantic guidance, not hard-coded trigger phrases.

When historical context matters and is not confidently present, retrieve before reconstructing.

## Quarterdeck / Engine Room

Normal agent-facing output should favor small local coordinates, conversational roles, source evidence, and minimal orientation.

Keep UUIDs, parent links, timestamps, branch topology, retrieval metadata, index metadata, embedding identity, build identity, and forensic provenance below deck unless needed.

Compact coordinates such as `@13` are local navigational handles, not durable identifiers. Durable message IDs remain below deck.

## Replay

Replay should stay close to original conversational information density. Storage roles may be projected for readability:

```text
user      -> you
assistant -> me
system    -> system
tool      -> tool
```

Role projection must not modify the message content itself or imply subjective identity, memory, or sameness.

## Observability

Keep diagnostics economical but sufficient to identify:

- runtime ACE version;
- semantic-contract version;
- current trusted chat binding;
- active/request-visible versus persisted coverage when relevant;
- semantic-canary visibility during development;
- retrieval success versus unresolved state.

Treat source artifact, tool registration metadata, model-visible schema, runtime implementation, and repository revision as separate observable seams.

## Dependency Strategy

Prefer Python standard library and Open WebUI application interfaces first. Add dependencies only after a measured requirement earns them.

Semantic search, PostgreSQL, pgvector, relational indexing, and distributed retrieval are candidates, not assumptions.

## Provenance

Maintain traceability:

```text
source transcript
    -> derived navigation
    -> candidate coordinate
    -> exact source evidence
    -> agent interpretation
```

Do not describe incomplete provenance as complete provenance.

## Collaboration

For durable work, prefer:

```text
propose / build
    -> inspect
    -> commit
    -> observe
    -> continue
```

Full-file generations may be built proactively when the design is coherent. Deployment remains an explicit operational gate. Use versioned handoff filenames and provide SHA-256 digests.

## Documentation Responsibilities

- `README.md`: human-facing purpose, current behavior, scope, and entry points.
- `CHANGELOG.md`: what changed by version.
- `AGENTS.md`: agent-facing invariants and working rules.
- `docs/ARCHITECTURE.md`: current architecture and principles.
- `docs/ADR/`: durable reasons for consequential decisions.

Do not turn ADRs into per-version diaries. When a decision changes, create a new ADR that supersedes the old one rather than rewriting decision history.
