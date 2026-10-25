# ACE Architecture

## Purpose

ACE lets a navigator find and replay exact evidence from a persisted Open WebUI conversation when relevant history is no longer confidently present in active context.

`README.md` is the shared project specification. This document describes the deeper architecture. `docs/ADR/` records why consequential choices were made.

## North Star

```text
navigator intent
    stochastic, interpretive, selective
            |
            v
ACE quarterdeck
    find + coordinate + canonical historical turns
            |
            v
ACE engine room
    trusted scope + source topology + sacred time
    pristine content + integrity + provenance
            |
            v
Open WebUI persisted chat
    authoritative source evidence
```

> Preserve richly below deck. Surface minimally above deck.

## Historical-Turn Contract

Normal resolved historical turns use:

```text
@<where> · <when> · <who>:
<what>
```

The contract is `turn-v1`.

`where` is navigation. `when` and `what` are projections of sacred source fields: time may be represented in another timezone but the source instant is never changed; content is not rewritten on evidence paths. `who` is a conversational projection of the stored role.

## Coordinates

ACE 0.3 continues to derive `@N` from current-trajectory position for compatibility with 0.2. This implementation is not yet sufficient to claim permanent lineage durability.

The accepted target contract is stronger: once a coordinate is durably minted within a lineage reference frame, it must never be rebound or reused. Durable mapping persistence and fork/ARC inheritance are intentionally deferred until the storage mechanism is observed and chosen.

Open WebUI message IDs remain below deck as source identifiers.

## Time Plane

Persisted source timestamps are sacred evidence.

ACE may:

- compare source timestamps;
- form temporal find windows;
- project a source instant into the navigator timezone for display;
- flag a disagreement between source trajectory and source time.

ACE may not synthesize, interpolate, correct, reorder, or replace historical time.

Timezone presentation precedence is browser request timezone, then user-profile timezone, then explicit UTC fallback.

Temporal find bounds use `[after, before)` semantics.

## Find Plane

`find` is the architectural navigation verb. The existing `ace_search_transcript` public tool retains its learned name.

Current find modes:

```text
lexical find   text condition over preserved turns
temporal find  source-time interval condition
combined find  lexical + temporal constraints
```

Future semantic, relational, and execution finds may extend this set. Every successful route should resolve back to canonical historical turns and exact source evidence.

Independent find results are ordered by sacred source time for presentation. The navigator's `find_order` UserValve chooses oldest-first or newest-first. This preference never changes source replay order.

## Replay Plane

Replay follows the reconstructed source trajectory, not timestamp sort order. Timestamp monotonicity is checked independently.

Exact-message and replay content is pristine relative to the persisted content Open WebUI exposes to ACE. Derived find excerpts may normalize whitespace because they are navigational clues.

## Integrity Plane

Integrity detection is observation, not repair.

Initial cheap detectors include:

```text
temporal.missing_source_timestamp
temporal.non_monotonic_trajectory
conversation.role_sequence
```

The detector architecture is intentionally extensible toward structural, coordinate, execution, and evidentiary findings.

A finding states what ACE can establish. It does not silently infer cause, severity, or remediation.

Execution history can contain relevant historical evidence. Ordinary replay should not become an execution trace, but execution evidence should be findable when the recall intent concerns commands/tools/APIs and the host preserved that evidence.

## Configuration Plane

Open WebUI UserValves provide navigator-level presentation preferences. ACE 0.3 introduces one:

```text
find_order = oldest_first | newest_first
```

The default is `oldest_first`.

Preferences are prohibited from modifying sacred source fields, coordinate bindings, replay topology, or integrity facts.

## Deterministic Footing, Stochastic Reasoning

ACE makes selected footing deterministic where practical:

```text
trusted current scope
source trajectory
source timestamp
coordinate resolution
persisted content
find constraints
integrity findings
resolved / unresolved state
```

Interpretation remains the navigator's job.

## Observability

Operational seams remain independent:

```text
artifact       version + digest
repository     exact revision
registration   visible tool metadata
schema         model-visible names/docstrings/parameters
runtime        ACE + contract versions + timezone source
history        find method + resolution + integrity findings
```

During beta the tool description carries the ACE release for a quick human check. Runtime diagnostics remain authoritative for the loaded implementation.

## Dependency Strategy

Prefer Python stdlib and Open WebUI application interfaces. `datetime` and `zoneinfo` provide temporal projection without introducing a new time dependency. System IANA timezone data availability is an environment dependency; UTC is the visible fallback.

Additional database/index/vector infrastructure remains future work that must be earned by measurement.

## Security

Normal retrieval remains current-chat scoped from trusted Open WebUI-injected context and the Open WebUI access-controlled chat interface. Model-supplied chat IDs are not authoritative. Cross-chat continuity requires its own authorization design.

## Decision Records

```text
0001 authoritative transcript
0002 trusted current-chat scope
0003 quarterdeck / engine-room separation
0004 agent-intent public tool surface
0005 search locates; replay establishes evidence
0006 observability at boundaries
0007 platform-native and stdlib first
0008 pristine evidence replay
0009 stable historical-turn grammar
0010 sacred time and trajectory integrity
```

When a decision changes, preserve history and supersede it with a new ADR.

## 0.3 Qualification Focus

1. Canonical header appears consistently across find, exact message, and replay.
2. Source content survives exact paths byte-for-byte as exposed by Open WebUI.
3. Same source instant renders correctly in navigator timezone and UTC fallback.
4. Temporal `[after, before)` boundaries behave deterministically.
5. Find ordering valve affects independent candidates only.
6. Replay remains topology-ordered even when timestamps disagree.
7. Integrity findings are visible and do not mutate evidence.
8. Model-facing semantics still cause uncertain memory to find/replay rather than reconstruct.
