# ADR-0009: Stable Historical-Turn Grammar

Status: Accepted

## Context

ACE can surface the same historical turn through lexical find, temporal find, exact retrieval, and replay. Continuity is weakened if each route teaches a different representation. Humans and agents also benefit from immediate temporal orientation, while the persisted timestamp and content must remain source evidence rather than material ACE rewrites.

## Decision

ACE uses one canonical historical-turn grammar:

```text
@<where> · <when> · <who>:
<what>
```

All four fields are mandatory for a resolved historical turn.

`where` is the ACE navigation coordinate. `when` is a display projection of the persisted source instant into the navigator timezone. `who` is a conversational role projection. `what` is persisted content.

Exact retrieval and replay preserve `what` pristine. ACE never manufactures or repairs historical timestamps. Temporal comparison uses recorded source timestamps, not display strings.

Independent find results may be presented oldest-first or newest-first. Replay remains in source trajectory order. If topology and recorded time disagree, ACE reports an integrity finding rather than reordering history.

## Consequences

The interface becomes a learned mnemonic: where, when, who, what. Retrieval machinery may evolve beneath it without changing the normal historical-turn grammar.

The mandatory frame costs a small number of tokens per turn. The cost is accepted for human orientation, agent orientation, and continuity.

Coordinate durability across lineage inheritance remains a stronger target than the current branch-position implementation. ACE must not claim that durability until a persistent coordinate mapping exists.
