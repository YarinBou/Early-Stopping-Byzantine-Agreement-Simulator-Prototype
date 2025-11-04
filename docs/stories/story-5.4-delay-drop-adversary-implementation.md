# Story 5.4: Delay/Drop Adversary Implementation

**Epic:** Epic 5 - Adversary Framework
**Week:** Weeks 10-12

## User Story

As a Delay/Drop adversary,
I want to introduce message delays and drops within synchrony bound Δ,
So that I can test protocol liveness under realistic network jitter.

## Acceptance Criteria

1. Create `DelayDropAdversary` class inheriting from `AdversaryStrategy`
2. Configuration: delay_distribution (Uniform, Normal, Pareto), drop_probability
3. `should_drop(message) -> bool` method using seeded RNG
4. `get_delay(message) -> float` method sampling from delay distribution
5. All delays capped at Δ (synchrony bound)
6. Dropped messages logged for audit
7. Unit tests covering: delay sampling, drop probability, Δ capping
8. Integration test: protocol maintains liveness despite delays/drops

## Prerequisites

Story 5.1

## Notes

Tests protocol under realistic network conditions.
