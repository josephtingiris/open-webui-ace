# ADR-0008: Preserve pristine evidence during exact replay

**Status:** Accepted

## Context

Message content can contain meaningful leading/trailing whitespace, newlines, indentation, quotes, backslashes, Unicode, code, or other formatting. ACE must not add noise or remove signal from evidence.

## Decision

We will return the persisted message content without ACE rewriting it on exact-message and replay paths. Search excerpts may normalize content because they are explicitly derived navigation aids.

## Consequences

Evidence paths must avoid stripping, whitespace normalization, re-indentation, Markdown cleanup, or intentional escaping/unescaping. ACE can claim fidelity only to the persisted content it receives from Open WebUI.
