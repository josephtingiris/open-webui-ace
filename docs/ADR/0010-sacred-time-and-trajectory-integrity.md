# ADR-0010: Sacred Time and Trajectory Integrity

Status: Accepted

## Context

Persisted conversations can contain anomalies caused by editing, migration, manual repair, host bugs, missing execution results, or unknown future conditions. A continuity engine must detect contradictions without manufacturing a cleaner past.

## Decision

Persisted source timestamps are sacred evidence. ACE may convert their representation for the navigator's timezone, but may not synthesize, interpolate, correct, or rewrite historical time.

Source topology determines replay order. Time is an independent integrity instrument. A disagreement between trajectory order and recorded time is surfaced as a finding and is never repaired by reordering or timestamp mutation.

Integrity checks are independent, cheap where practical, and extensible. Initial families include structural, coordinate, temporal, conversational, execution, and evidentiary integrity. A finding reports observation; it does not automatically prove corruption or prescribe repair.

ACE never mutates evidence merely to satisfy an integrity invariant.
