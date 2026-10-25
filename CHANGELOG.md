# Changelog

All notable ACE changes are recorded here. ADRs explain consequential architectural decisions.

## 0.3.0

### Added

- Canonical historical-turn grammar: `@where · when · who: what`.
- Human-oriented local timestamp presentation derived from persisted source time.
- Browser timezone -> profile timezone -> UTC fallback projection.
- Optional `[after, before)` source-time bounds on `ace_search_transcript` for temporal find.
- `find_order` UserValve with `oldest_first` default and `newest_first` alternative for independent find results.
- Cheap temporal and conversational integrity findings.
- Historical-turn and coordinate contract identifiers in runtime diagnostics.
- Visible `ACE 0.3.0` marker in tool-level description during Zero Day/beta.
- ADR-0009 and ADR-0010.

### Changed

- Search/find, exact-message, and replay surfaces use the same turn header.
- Replay preserves source trajectory order while time is checked independently for anomalies.
- README is the common human/agent project specification; AGENTS.md is retired.
- Architectural vocabulary prefers `find` for locating an X while the existing public `ace_search_transcript` name remains stable.

### Integrity

- ACE reports missing source timestamps and non-monotonic trajectory time rather than manufacturing or correcting history.
- Repeated conversational roles are surfaced as cheap diagnostic findings, not automatic proof of corruption.

### Preserved

- Exact-message and replay content remains pristine as established by 0.2.1.
- Current-chat trusted scope and access-control boundary remain unchanged.

## 0.2.1

### Fixed

- Preserve leading and trailing whitespace in exact message retrieval and replay.

## 0.2.0

### Added

- Compact `@position` navigation coordinates.
- Conversational `you` / `me` role projection.
- Runtime contract and semantic-canary diagnostics.
- Explicit unresolved lexical results.

## 0.1.0

- First working trusted current-chat lexical retrieval and bounded replay prototype.
