# Open WebUI Agent Continuity Engine (ACE)

ACE gives an agent and a human peer a small set of instruments for finding and replaying preserved evidence from the current Open WebUI conversation when relevant history is no longer confidently present in active context.

> Trustworthy recall beats plausible reconstruction.

## Current Release

ACE 0.3.0 is the temporal-positioning generation. It adds canonical historical-turn presentation, sacred source-time handling, temporal find bounds, a first per-user presentation valve, and cheap trajectory-integrity findings.

## Core Invariants

1. The persisted Open WebUI transcript is authoritative evidence for what occurred.
2. Normal scope comes from trusted Open WebUI-injected current-chat context.
3. Derived indexes, summaries, excerpts, embeddings, and relationships are navigation aids, not replacements for evidence.
4. Plausible reconstruction is not recovered evidence; unresolved is legitimate.
5. ACE may project evidence for navigation. ACE may not mutate evidence to satisfy an invariant.
6. Persisted source content is sacred on exact-message and replay paths.
7. Persisted source timestamps are sacred. ACE may convert their visible timezone representation but must never synthesize, interpolate, correct, or rewrite historical time.
8. Source topology orders replay. Timestamp disagreement is an integrity finding, never permission to reorder history.
9. ACE coordinates such as `@60` are navigation coordinates. Once a durable lineage mapping is introduced, assigned coordinates must never be rebound or reused.
10. Continuity, recovery, inheritance, and retrieval do not establish identity or sameness.
11. Cross-chat retrieval requires a separately designed authorization boundary.
12. Prefer simple deterministic machines and platform-native interfaces; add infrastructure only when measurement earns it.

## Canonical Historical Turn

ACE 0.3 uses one grammar wherever a historical turn is surfaced:

```text
@<where> · <when> · <who>:
<what>
```

Example:

```text
@60 · Oct 25, 9:13 AM EDT · you:
persisted message content
```

- **where**: ACE navigation coordinate.
- **when**: human-oriented projection of the persisted source instant into the current navigator timezone.
- **who**: `user -> you`, `assistant -> me`; other stored roles remain literal.
- **what**: source content. Exact-message and replay paths do not rewrite it.

The timestamp displayed by ACE is a representation of the recorded source instant, not a replacement timestamp.

## Finding and Replay

Architecturally, ACE **finds** an X, resolves its coordinate, then replays source evidence.

The current public surface remains intentionally stable:

```text
ace_check_context
ace_get_chat
ace_search_transcript
ace_get_message
ace_get_context
```

`ace_search_transcript` performs lexical find, temporal find, or both. It keeps its established public name for compatibility.

Temporal bounds are absolute source timestamps and use `[after, before)` semantics: inclusive lower bound, exclusive upper bound.

Independent find results default to oldest-first. A per-user `find_order` valve can select newest-first. The valve affects only independent result presentation; it cannot reorder source replay or alter evidence.

## Evidence Fidelity

Navigation excerpts may normalize whitespace because they are clues. Exact-message retrieval and replay return persisted content without ACE calling `strip()`, collapsing whitespace, cleaning Markdown, changing Unicode, or otherwise rewriting the evidence.

ACE can preserve only what Open WebUI exposes to it. Do not claim origin or completeness that the source cannot establish.

## Time

ACE carries recorded time; it does not create historical time.

Display timezone resolution is:

```text
browser timezone
-> user-profile timezone
-> explicit UTC fallback
```

Temporal comparisons operate on source timestamps, never on rendered strings.

## Integrity

Integrity detection is extensible and independent from repair. ACE 0.3 starts with cheap findings for:

- missing source timestamps;
- non-monotonic source time along the reconstructed trajectory;
- unexpected repeated `user` or repeated `assistant` roles in the conversational projection.

A finding means something deserves attention. It does not by itself establish corruption, cause, or severity. ACE surfaces anomalies and does not silently repair sacred records.

Execution/tool-call integrity is an explicit extension point. Execution evidence should be recoverable when the user's historical intent concerns commands or tools and when Open WebUI preserved that evidence; missing expected execution evidence must not be reconstructed.

## Public Tool Semantics

Public methods name agent intentions using `ace_<action>_<object>`. Names, docstrings, and parameter descriptions are part of the learned interface. Spend them carefully.

When historical context matters and is not confidently present, find/replay evidence before reconstructing.

## Quarterdeck / Engine Room

Above deck, favor coordinates, local time, roles, pristine evidence, and calm integrity notices.

Below deck, retain UUIDs, parent links, source timestamps, branch topology, execution structures, retrieval metadata, and provenance needed to establish those views.

## Observability

Operational seams are separate and should be independently observable:

- artifact version/digest;
- repository revision;
- Open WebUI registration metadata;
- model-visible tool schema;
- runtime ACE version/contracts;
- timezone projection source;
- retrieval success/unresolved state;
- trajectory-integrity findings.

During Zero Day/beta the tool-level description carries the ACE version for a quick human integration-screen check. `ace_check_context` remains runtime truth.

## Project Context

ACE is developed under the Infinite Continuity Experiment (ICE). An Agent Recovery Core (ARC) is a separate recoverable continuity asset associated with an agent lineage/version. ACE may eventually participate in ARC workflows, but ARC generation remains outside the current implementation.

```text
agent != ARC
lineage != session
continuity != identity
inheritance != sameness
```

> Continuity without requiring sameness.

## Collaboration

Work from observed evidence. Distinguish observed behavior, documented platform behavior, accepted decisions, working hypotheses, and future possibilities.

For durable work:

```text
propose / build -> inspect -> commit -> observe -> continue
```

Deployment remains an explicit operational gate. For handoffs, use versioned filenames and SHA-256 digests.

## Documentation

- `README.md`: common front door and shared project specification for humans and agents.
- `CHANGELOG.md`: what changed by version.
- `docs/ARCHITECTURE.md`: deeper current architecture.
- `docs/ADR/`: durable reasons for consequential decisions.

There is intentionally no separate agent specification.

## Status

Experimental. Zero Day. ACE 0.3.0 is ready for live qualification; behavior not yet observed live should not be described as proven.
