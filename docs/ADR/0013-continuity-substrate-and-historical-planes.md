# ADR-0013: Continuity Substrate and Historical Planes

Status: Accepted as architectural direction

## Context

The first Open WebUI ACE focused on saved conversational messages. Live qualification showed that host history may also include reasoning traces, tool activity, results, timestamps, topology, and artifacts.

Treating the transcript as the entire continuity foundation would confuse the first useful source with the broader infrastructure problem.

## Decision

Treat host-retained history as potentially multi-plane:

```text
dialogue
time
topology
reasoning
actions
results
artifacts
```

An ACE provides a continuity interface that selectively moves bounded, source-grounded historical material into current context.

The current Open WebUI ACE contract remains message-focused. Reasoning, action, result, and artifact navigation are future capabilities until separately implemented and qualified.

Preserved sources remain distinct from derived maps. Reasoning traces must never be described as complete cognition, and missing traces must never be reconstructed as recovered history.

## Consequences

The architecture is no longer defined as transcript search, although exact message find/replay remains the first production-shaped service.

Future historical planes require explicit provenance, authorization, presentation, search, replay, and retention contracts before entering the public surface.
