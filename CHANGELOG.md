# Changelog

All notable ACE changes are recorded here. This file describes what changed; architecture decision records explain why.

## Unreleased

### Fixed

- Preserve leading and trailing whitespace in exact message retrieval and replay. This is planned for the 0.2.x line and corrects a fidelity defect found during 0.2.0 review.

### Operational

- Use versioned downloadable artifact names and SHA-256 digests for full-generation handoffs.
- Make runtime version, semantic contract, and tool-schema freshness observable at separate boundaries.

## 0.2.0

### Added

- Compact `@position` coordinates for normal agent navigation.
- Conversational replay labels: persisted `user` is surfaced as `you`; persisted `assistant` is surfaced as `me`.
- Runtime version, semantic-contract, and semantic-canary diagnostics.
- Stronger model-visible guidance for natural continuity intents such as remembering, looking back, and recovering earlier conversation.
- Explicit unresolved results for failed lexical searches and invalid coordinates.

### Changed

- Normal retrieval output was reduced substantially; UUIDs, parent identifiers, timestamps, and branch machinery remain below deck.
- Context retrieval became replay-shaped output close to the original conversation rather than database-shaped JSON.
- `ace_get_chat` became a compact continuity-coverage diagnostic rather than a transcript dump.
- Tool guidance explicitly prefers ACE retrieval over guessing, URL fetching, and plausible reconstruction for current-chat historical evidence.

### Observed

- Moss, ACE Patient Zero, autonomously selected a historical event, used lexical search to locate a compact coordinate, replayed its neighborhood, and reasoned forward from recovered evidence.
- Installation testing showed that runtime source, tool registration metadata, model-visible schema, and artifact identity are separate operational seams worth observing.

### Known issue

- Exact-message and replay paths call `strip()` in 0.2.0, which can alter leading or trailing whitespace. Search normalization is intentional; evidence mutation is not.

## 0.1.0

### Added

- First working ACE Workspace Tool.
- Trusted current-chat binding through Open WebUI-injected context.
- Access-controlled persisted-chat loading through Open WebUI application interfaces.
- Case-insensitive substring search.
- Exact-message retrieval and bounded surrounding-context retrieval.
- `ace_check_context` diagnostic surface.

### Observed

- Workspace Tool invocation received a nonempty trusted chat identifier.
- Persisted transcript search successfully returned exact historical coordinates and excerpts.
- Returned coordinates successfully reopened exact messages and surrounding neighborhoods.
- Early model tool selection sometimes substituted generic `fetch_url` for retrieval-oriented ACE tools, motivating stronger semantic guidance in 0.2.0.
