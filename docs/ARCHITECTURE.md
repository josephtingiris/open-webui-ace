# ACE Architecture

## Purpose

This document records the architecture of the Open WebUI Agent Continuity Engine (ACE), with emphasis on why the system is being built this way.

ACE is an experimental continuity capability for agents operating through Open WebUI. Its first objective is narrow: let an agent locate and reopen exact evidence from its own persisted current-chat transcript when relevant history is no longer useful or available in active model context.

This document distinguishes observed behavior from design decisions and future possibilities. Planned behavior is not implemented behavior.

## Architectural North Star

ACE separates a small agent-facing continuity interface from a richer deterministic evidence and retrieval layer.

```text
agent reasoning
    stochastic, interpretive, selective
            |
            v
ACE quarterdeck
    small semantic tool surface
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

The working principle is:

> Preserve richly below deck. Surface minimally above deck.

The agent should experience continuity, not database administration.

## Current Proven Architecture

The first live ACE experiments established the following on the test Open WebUI deployment:

1. A Workspace Tool can receive an Open WebUI-injected current chat identifier through `__chat_id__`.
2. The injected chat identifier can identify the current persisted chat without asking the model to provide a chat ID.
3. ACE can retrieve the current persisted chat through Open WebUI's own access-controlled application interface.
4. ACE can reconstruct the active message branch from persisted messages.
5. ACE can perform case-insensitive lexical search over that branch.
6. A search result can be used to reopen one exact persisted message.
7. The same historical coordinate can be used to reopen a bounded neighborhood around that message.
8. Natural-language continuity intent can cause an agent to select ACE retrieval tools autonomously.
9. Diagnostic and retrieval operations can coexist in the same Workspace Tool.

These findings establish feasibility for the first ACE implementation. They do not establish semantic retrieval, cross-chat retrieval, ARC generation, lineage identity, or indefinite retention.

## Authoritative Evidence

The persisted Open WebUI chat transcript is authoritative for what occurred in the chat.

ACE may later maintain indexes, embeddings, summaries, caches, relationships, or other derived representations, but those structures are navigational aids. They are not replacements for source evidence.

```text
derived retrieval result
        -> historical coordinate
        -> exact persisted message
        -> surrounding transcript when needed
```

A plausible reconstruction is not recovered evidence.

When ACE cannot establish the remembered event from source evidence, unresolved retrieval is preferable to confident invention.

## Trusted Scope

Normal ACE retrieval is scoped from trusted context injected by Open WebUI.

The model does not choose the authoritative chat identifier for ordinary current-chat retrieval.

This matters for both correctness and isolation:

```text
Open WebUI request
    -> injected chat coordinate
    -> access-controlled current chat
    -> ACE retrieval
```

A future cross-chat or cross-session capability requires an explicit architecture and authorization boundary. It must not emerge accidentally by accepting arbitrary model-supplied chat identifiers.

## Platform Boundary

ACE prefers Open WebUI's application interfaces over direct database access when an appropriate interface exists.

The present implementation uses Open WebUI's access-controlled chat lookup rather than treating SQLite as the authorization boundary.

Reasons:

- ownership and sharing policy remain Open WebUI responsibilities;
- ACE avoids duplicating host authorization logic;
- storage implementation can evolve independently from the agent-facing ACE contract;
- the retrieval code expresses intent at the application level rather than depending unnecessarily on database layout.

Direct storage access remains a possible diagnostic or future performance technique, not the default trust boundary.

## Public Tool Surface

Public ACE methods describe agent intentions. Private methods describe mechanisms.

The public naming grammar is:

```text
ace_<action>_<object>
```

The initial action vocabulary is intentionally small:

```text
check   diagnostics or validation
get     retrieve a known object or state
list    enumerate
search  locate candidate historical coordinates
set     alter explicitly ACE-owned state
index   build or refresh derived retrieval state
```

Examples presently under development include:

```text
ace_check_context
ace_get_chat
ace_search_transcript
ace_get_message
ace_get_context
```

Implementation details remain private:

```text
_load_current_chat
_lexical_search
_semantic_search
_reconstruct_branch
```

This permits ACE to replace storage, indexing, ranking, or embedding mechanisms without unnecessarily changing the vocabulary exposed to agents.

## Tool Semantics Are Architecture

An agent sees tool names, descriptions, and parameter descriptions before choosing whether and how to use a tool. Those fields are therefore part of ACE's behavioral interface, not decorative documentation.

ACE descriptions should teach useful continuity behavior, including when to search preserved history rather than reconstruct from plausibility.

Important continuity intents include natural requests such as:

```text
do you remember ...
what did we say earlier ...
we talked about ...
look back ...
find when ...
what happened before ...
```

These examples guide semantics; ACE should not depend on hard-coded phrase triggers.

The intended behavioral rule is:

> When historical context matters and is not confidently present, retrieve before reconstructing.

## Semantic Contract Validation

Because tool descriptions influence agent behavior, ACE should be able to verify both the running implementation and the model-visible semantic contract.

Two complementary observations are useful:

```text
runtime identity
    Which ACE build executed?

semantic identity
    Which tool guidance did the model actually receive?
```

The diagnostic surface may therefore expose a compact build identifier and semantic-contract identifier.

During development, unique low-cost semantic canaries may be placed in model-visible tool descriptions and queried without calling the tool. This helps distinguish stale code, stale schemas, and unexpected model behavior.

Operational telemetry belongs primarily in diagnostics, not normal retrieval output.

## Quarterdeck and Engine Room

ACE intentionally separates the information needed for reasoning from the information needed for machinery and forensics.

### Quarterdeck

Normal agent-facing retrieval should favor:

```text
small local coordinate
role
source evidence or excerpt
minimal orientation
```

### Engine room

ACE may retain or use:

```text
chat UUIDs
message UUIDs
parent links
branch topology
timestamps
storage metadata
retrieval method
index metadata
embedding model and version
provenance
build identity
diagnostic measurements
```

Rich provenance being available does not require rich provenance to be injected into every reasoning cycle.

## Economical Continuity

ACE should optimize the amount of history surfaced to the agent, not merely the speed or size of the database query.

The desired agent-facing information density is close to the original conversation:

```text
user:
original content

assistant:
original content
```

Sequence is usually conveyed by order. UUIDs, parent identifiers, and timestamps should remain below deck unless they are needed for navigation, diagnostics, provenance, or an explicitly requested forensic view.

A retrieval interface should progressively disclose information:

```text
search
    small candidate handles + short excerpts

replay
    roles + exact original content

provenance
    durable identifiers + structure when explicitly needed

diagnostics
    implementation and runtime observations
```

This preserves fidelity while reducing serialization, rendering, token, and reasoning overhead.

## Coordinates

Open WebUI message UUIDs are durable machine coordinates but expensive agent-facing symbols.

ACE may expose compact local coordinates such as short branch positions or retrieval handles while retaining durable UUID mappings below deck.

A compact coordinate must not silently be treated as more stable than it is. Branching, regeneration, deletion, or other transcript changes may affect positional coordinates.

Therefore:

> Durable coordinates live below deck. Local coordinates may be used as lightweight navigational handles above deck.

The stability properties of compact coordinates must be measured before they become a durable public contract.

## Search and Replay

Search and replay serve different cognitive roles.

### Search

Search answers:

> Where should I look?

It may be lexical now and semantic or hybrid later. Search returns candidate locations, not historical truth claims.

### Replay

Replay answers:

> What actually happened here?

Replay should approach the information density of the original conversational turns. It should avoid repeating database structure that is not needed for understanding.

This distinction allows fuzzy navigation later without making the historical evidence fuzzy.

## Deterministic Footing, Stochastic Reasoning

ACE does not attempt to make agent reasoning deterministic.

Interpretation, association, judgment, and search strategy may remain stochastic. ACE makes selected footing deterministic where practical:

```text
which build ran
which chat was bound
which source coordinate was recovered
which exact evidence exists there
which retrieval method produced a candidate
whether retrieval succeeded or remained unresolved
```

The purpose is not deterministic thought.

> The purpose is deterministic footing for fluid thought.

## Observability

Observability is a first-class architecture concern because failures and surprises occur at system boundaries.

Useful boundaries include:

```text
Open WebUI -> model
    tool names, descriptions, parameter schemas

model -> Open WebUI
    selected tool and arguments

Open WebUI -> ACE
    injected trusted context

ACE -> persistence
    retrieved source and branch

ACE -> model
    amount and form of evidence surfaced
```

ACE should instrument these boundaries economically. Normal retrieval output should remain quiet.

`ace_check_context` is retained as a deliberate diagnostic instrument rather than discarded after initial development.

## Dependency Strategy

ACE begins with Python's standard library and the interfaces already provided by Open WebUI.

Additional dependencies must earn their place through a measured requirement.

This does not prohibit substantial infrastructure. It establishes an order of operations:

```text
platform primitives
    -> exact retrieval
    -> measure failure and scale
    -> add the next required mechanism
```

Potential future infrastructure includes PostgreSQL, full-text indexing, embeddings, `pgvector`, relational indexes, and distributed storage or retrieval systems. These are candidates, not current assumptions.

## Scale and Retention

The Infinite Continuity Experiment (ICE) may intentionally try to preserve, index, carry forward, and retrieve as much earned history as practical for as long as practical.

ACE should not assume forgetting is required merely because biological memory forgets.

At the same time, active model context remains finite. ACE therefore separates retention from carriage:

> Keep the present small while extending what the present can reach.

Storage scale and retrieval scale are engineering problems to measure and push outward. The first implementation should not prematurely impose irreversible forgetting policies.

## Security Posture

Workspace Tools execute with substantial server-side capability. ACE should exercise less privilege than its host may technically provide.

Current rules:

- scope normal retrieval from trusted injected context;
- use Open WebUI's access-control boundary;
- do not return authentication material;
- do not expose complete injected user or request objects;
- do not expose another chat through accidental scope expansion;
- keep rich structural metadata below deck unless needed;
- do not claim isolation that has not been tested.

Broad host capability is not a reason for broad ACE behavior.

## Current Decision Record

### D001 - Persisted transcript is authoritative

**Decision:** Treat the persisted Open WebUI transcript as source evidence for what occurred.

**Why:** Derived representations can be useful for navigation but can also omit, compress, or distort the lived path.

**Consequence:** Search results should remain traceable to exact persisted messages.

**Status:** Active.

### D002 - Current-chat scope comes from trusted injected context

**Decision:** Use Open WebUI-injected current-chat context for normal retrieval scope.

**Why:** The model should not be responsible for supplying its own authorization coordinate.

**Consequence:** Cross-chat retrieval requires a separate explicit design.

**Status:** Active and empirically demonstrated.

### D003 - Preserve richly below deck, surface minimally above deck

**Decision:** Keep structural and provenance detail available internally while minimizing normal agent-facing output.

**Why:** UUIDs, topology, timestamps, and index metadata are useful machinery but expensive cognitive and token baggage.

**Consequence:** ACE needs progressive disclosure and compact local navigation.

**Status:** Active.

### D004 - Public API names agent intent

**Decision:** Public tool methods use the `ace_<action>_<object>` grammar and describe agent intentions rather than implementation mechanisms.

**Why:** Tool names and descriptions are part of the model's decision surface.

**Consequence:** Storage and ranking mechanisms can evolve behind stable semantic operations.

**Status:** Active.

### D005 - Search locates; replay establishes evidence

**Decision:** Treat search results as candidate coordinates and exact replay as source evidence.

**Why:** A plausible or similar result is not automatically the remembered event.

**Consequence:** ACE should support an honest unresolved state when evidence is not established.

**Status:** Active.

### D006 - Observability is a first-class boundary

**Decision:** Retain economical diagnostics for runtime identity, semantic contract, trusted scope, and retrieval behavior.

**Why:** Correct operation depends on several boundaries that can fail independently.

**Consequence:** Diagnostic instrumentation remains available without burdening normal retrieval output.

**Status:** Active.

### D007 - Prefer platform-native and standard-library mechanisms first

**Decision:** Start with Python stdlib and Open WebUI application interfaces before adding external retrieval infrastructure.

**Why:** Requirements should be demonstrated before dependencies become architectural commitments.

**Consequence:** PostgreSQL, vector search, and other systems remain available when scale or retrieval quality earns them.

**Status:** Active.

## Near-Term Architecture Work

The next generation should focus on the continuity interface rather than additional storage infrastructure:

1. Compact search result handles.
2. Replay-shaped context with minimal structural JSON.
3. Stronger model-visible guidance for continuity intents.
4. Runtime and semantic-contract identifiers in diagnostics.
5. Explicit unresolved behavior.
6. Tests across active-context boundaries, forks, invalid coordinates, common searches, and high-match searches.

Semantic search and external indexing should follow measured lexical and scale failures rather than precede them.
