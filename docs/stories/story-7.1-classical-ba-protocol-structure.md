# Story 7.1: Classical BA Protocol Structure

**Epic:** Epic 7 - Classical Baseline Implementation
**Week:** Weeks 13-14

## User Story

As a baseline implementer,
I want a simple classical BA protocol with (t+1) round bound,
So that I can compare against early-stopping protocol under identical conditions.

## Acceptance Criteria

1. Create `classical_ba.py` module with `ClassicalBA` class
2. Simpler structure than early-stopping: no GDA, simpler threshold logic
3. Classical termination: decision guaranteed by round t+1
4. Reuse existing infrastructure: Message schema, crypto, round scheduler
5. Protocol logic: reliable broadcast + decision after sufficient evidence
6. Unit tests covering: initialization, basic execution structure
7. Docstrings explaining classical (t+1) bound vs. early-stopping (1+ε)f

## Prerequisites

Story 1.9

## Notes

Baseline for empirical comparison with early-stopping.
