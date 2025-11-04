# Story 2.6: Deterministic Asyncio Scheduling

**Epic:** Epic 2 - Round Scheduler & Synchrony Model
**Week:** Weeks 2-4

## User Story

As a researcher,
I want deterministic asyncio task scheduling with seeded randomness,
So that experimental runs are reproducible with identical seeds.

## Acceptance Criteria

1. Create `determinism.py` module with seeded RNG management
2. `set_seed(seed: int)` function configuring global random seed (Python `random`, `numpy` if used)
3. Asyncio task scheduling order made deterministic (use task IDs or explicit ordering)
4. Message delivery order deterministic when multiple messages arrive simultaneously
5. Document any sources of non-determinism (e.g., asyncio internal scheduling)
6. Reproducibility test: same seed produces identical round-by-round message sequences
7. Unit tests covering: seeded execution, reproducible random choices
8. Integration test: two runs with same seed produce bit-identical message delivery order

## Prerequisites

Story 2.2

## Notes

Critical for reproducibility - enables bit-identical experimental reproduction.
