# Story 2.1: Basic Round Scheduler with Asyncio

**Epic:** Epic 2
**Week:** Weeks TBD

## User Story

As a simulation engine,
I want lock-step round coordination using asyncio,
So that all nodes progress through rounds synchronously with controlled timing..

## Acceptance Criteria

1. Create `scheduler.py` module with `RoundScheduler` class
2. `__init__(n: int, delta: float)` constructor with node count and timeout bound Δ
3. `advance_round()` async method incrementing current round counter
4. `get_current_round() -> int` method returning current round
5. Asyncio coordination: all nodes wait at round boundary before advancement
6. Basic round progression test: advance through multiple rounds deterministically
7. Unit tests covering: initialization, round advancement, current round tracking
8. Docstrings explaining synchronous model and Δ timeout semantics

## Prerequisites

Story 1.1
