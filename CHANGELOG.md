# Changelog

## Unreleased

### Documentation

- Rebuild the README front door around the ordered promise: extend context, enhance capabilities, and do so economically.
- Define ACE as the project, an ACE as one Agent Continuity Engine, and this repository as the Open WebUI ACE.
- Clarify that Open WebUI owns saved conversations while the Open WebUI ACE selectively finds and replays earlier messages.
- Reframe the architecture around a host-owned continuity substrate with multiple possible historical planes.
- Record economic design as a measurable objective rather than an unqualified cost claim.
- Add ADR-0012 and ADR-0013.

## 0.3.1

### Changed
- Replace experimental `@N` historical coordinates with `~N` for live qualification.
- Keep coordinate meaning and `trajectory-v1` resolution unchanged.
- Treat `~N` as provisional notation, not a durable lineage-coordinate claim.

### Rationale
- `@` is heavily occupied by chat mention semantics and the Open WebUI input surface.
- `~` inherits useful home, contextual-resolution, relative-location, relationship, and approximation semantics worth testing in practice.

## 0.3.0
- Added canonical historical-turn grammar, local timestamp projection, temporal find bounds, find-order UserValve, and initial integrity findings.

## 0.2.1
- Preserve leading and trailing whitespace in exact retrieval and replay.

## 0.2.0
- Added compact trajectory coordinates and conversational replay.

## 0.1.0
- First working trusted current-chat lexical retrieval and bounded replay prototype.
