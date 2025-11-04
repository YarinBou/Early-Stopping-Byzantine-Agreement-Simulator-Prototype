# Story 7.3: Baseline Experimental Parity

**Epic:** Epic 7 - Classical Baseline Implementation
**Week:** Weeks 13-14

## User Story

As a researcher,
I want classical baseline using identical experimental conditions,
So that comparisons are fair (same n, t, f, Δ, adversaries).

## Acceptance Criteria

1. Classical BA uses same `RoundScheduler` with identical Δ
2. Classical BA uses same adversary framework (Equivocator, Withholder, Delay/Drop)
3. Classical BA uses same message acceptance pipeline
4. Classical BA uses same metrics collection (rounds, messages, crypto ops)
5. Configuration parity: run classical and early-stopping with identical parameters
6. Unit tests covering: shared infrastructure usage
7. Integration test: both protocols run on same (n, t, f) configuration, produce comparable metrics

## Prerequisites

Stories 2.8, 5.6, 7.2

## Notes

Ensures fair comparison between classical and early-stopping.
