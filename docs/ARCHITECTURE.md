# ACE Architecture

## Purpose

ACE is a project exploring Agent Continuity Engines.

The Open WebUI ACE lets agents find and selectively replay saved messages from the current Open WebUI conversation when earlier history is no longer confidently available in active context.

> Extend your context. Enhance your capabilities. Economically.

## Architectural North Star

An ACE lets a finite navigator participate in a history much larger than any active context.

```text
host-owned recorded history
            |
            v
ACE continuity interface
    find + resolve + replay
            |
            v
bounded current context
            |
            v
navigator reasons and acts
            |
            v
new recorded history
```

The host platform owns storage, schema, lifecycle, and access control. An ACE provides continuity movement between recorded history and current context.

## Project, Pattern, and Implementation

```text
ACE project
    explores Agent Continuity Engines

an ACE
    one engine implementing the pattern

the Open WebUI ACE
    this repository's host-specific implementation
```

The architecture should permit future ACEs on other platforms without pretending that their source schemas, permissions, or retained historical planes are identical.

## Current Source Boundary

Open WebUI is authoritative for the records it exposes to this implementation. The Open WebUI ACE does not claim to create or own those records.

Current replay uses saved message content plus host-provided message identity, role, timestamp, and trajectory topology.

```text
Open WebUI
    conversation persistence
    message schema
    access control
    branch topology
    source timestamps
            |
            v
Open WebUI ACE
    trusted scope
    deterministic coordinates
    find constraints
    source replay
    integrity observations
```

## Historical Planes

A saved historical turn may contain more than visible dialogue. Host platforms may preserve several planes:

```text
dialogue     what was said
time         when it was recorded
topology     where it sits in the source trajectory
reasoning    what reasoning trace the host retained
actions      what tools or operations were attempted
results      what those actions returned
artifacts    what durable outputs were produced
```

ACE 0.3.1 exposes the dialogue, time, and topology needed for message find/replay and initial integrity findings. Reasoning, action, result, and artifact navigation are extension directions, not current public contracts.

A preserved reasoning trace is not complete cognition. A missing trace does not establish that no reasoning occurred. An ACE must replay only what the host retained and must not reconstruct missing private or hidden reasoning.

## Quarterdeck and Engine Room

Above deck, favor calm, compact navigation:

```text
~<where> · <when> · <who>:
<what>
```

Below deck, retain the source structures needed to establish that projection:

```text
message IDs
parent/child links
source timestamps
stored roles
structured outputs
execution metadata
retrieval provenance
contract versions
integrity findings
```

Preserve richly below deck. Surface minimally above deck.

## Coordinate Plane

The Open WebUI ACE currently derives `~N` from position on the current source trajectory. This is useful navigation but is not yet a durable lineage-coordinate implementation.

The accepted long-term invariant is stronger:

> Once a coordinate is durably minted in a lineage reference frame, it must never be rebound or reused.

A coordinate is a bearing resolved within a reference frame. It is not the saved record itself.

Open WebUI message IDs remain below deck as source identifiers.

## Find Plane

`find` is the architectural navigation verb. The public `ace_search_transcript` name remains for learned-interface compatibility.

Current modes:

```text
lexical find   text condition over saved messages
temporal find  source-time interval condition
combined find  lexical + temporal constraints
```

Independent findings may be presented oldest-first or newest-first. Presentation order never changes source replay order.

Future semantic, relational, reasoning, execution, and artifact finds must resolve back to host-retained sources with explicit provenance.

## Replay Plane

Replay follows source trajectory topology, not timestamp sort order.

Exact-message and surrounding-context replay preserve saved content as exposed by Open WebUI. Navigation excerpts may normalize whitespace because they are clues rather than source replay.

```text
find candidate
-> resolve coordinate
-> replay saved source
-> continue present work
```

## Time Plane

Recorded source timestamps are sacred records.

The Open WebUI ACE may:

- compare source timestamps;
- form `[after, before)` temporal find windows;
- project a source instant into the navigator's timezone;
- report disagreement between source time and source trajectory.

It may not synthesize, interpolate, correct, reorder, or replace historical time.

Timezone display precedence is browser timezone, then user-profile timezone, then explicit UTC fallback.

## Integrity Plane

Integrity detection is observation, not repair.

Current finding types include:

```text
temporal.missing_source_timestamp
temporal.non_monotonic_trajectory
conversation.role_sequence
```

A finding says what the Open WebUI ACE can establish from the available source. It does not silently infer cause, severity, or remediation.

## Economic Design

The Open WebUI ACE extends effective context through selective replay rather than permanent residency of the whole conversation in active context.

```text
large saved conversation
        |
        v
cheap deterministic find
        |
        v
bounded replay
        |
        v
current context
```

Economic design includes more than token count:

- less human repetition and catch-up;
- bounded context introduced per recovery;
- lower avoidable model processing;
- measured retrieval latency;
- rebuildable derived indexes;
- early exit when current context is sufficient;
- graceful unresolved results instead of expensive invention.

These are design objectives. Strong cost claims require measurement under representative workloads.

## Derived Maps

Indexes, summaries, excerpts, embeddings, relationship graphs, and caches may improve navigation. They remain disposable accelerators.

```text
sources
    authoritative within established provenance

derived maps
    versioned
    replaceable
    rebuildable
    allowed to be stale only when disclosed and bounded
```

Derived state must not silently replace, mutate, or outrank its source.

## Security and Scope

Current retrieval remains scoped to the invoking Open WebUI conversation using trusted injected context and Open WebUI's access-controlled chat interfaces.

Model-supplied chat IDs are not authoritative. Cross-conversation or cross-platform continuity requires explicit authorization, provenance, and lineage boundaries.

## Observability

Operational seams should remain independently observable:

```text
artifact       version + digest
repository     exact revision
registration   visible tool metadata
schema         model-visible names/docstrings/parameters
runtime        ACE + contract versions
time           timezone source
history        find method + resolution state
integrity      findings without silent repair
economy        latency + bounded context + derived-map cost
```

## Extension Discipline

ACE begins with saved messages because they solve a real continuity problem and are available through Open WebUI's current interfaces.

New planes and infrastructure must be earned by observed need and measurement. The architecture should avoid assumptions that forbid later scale:

- all history need not be locally resident;
- one process need not own truth;
- coordinates must not become accidental global list offsets;
- search need not mean scanning everything;
- one index must not become authoritative history;
- failure of a derived subsystem must not manufacture replacement history.

## Decision Records

```text
0001 authoritative transcript
0002 trusted current-chat scope
0003 quarterdeck / engine-room separation
0004 agent-intent public tool surface
0005 search locates; replay establishes source
0006 observability at boundaries
0007 platform-native and stdlib first
0008 pristine evidence replay
0009 stable historical-turn grammar
0010 sacred time and trajectory integrity
0011 tilde coordinate notation experiment
0012 project and engine vocabulary
0013 continuity substrate and historical planes
```

Earlier ADR titles preserve the vocabulary of the phase in which they were accepted. When a decision changes, preserve history and supersede it rather than rewriting the past.

## Current Qualification Focus

1. `~N` renders and resolves consistently in real Open WebUI use.
2. Exact saved content survives replay as exposed by Open WebUI.
3. Source instants render correctly across timezone paths.
4. Temporal bounds and find ordering remain deterministic.
5. Replay remains topology-ordered when timestamps disagree.
6. Integrity findings remain observational.
7. Agents use continuity tools when needed rather than reconstructing history.
8. Economic claims are instrumented before they are promoted from hypothesis to promise.
