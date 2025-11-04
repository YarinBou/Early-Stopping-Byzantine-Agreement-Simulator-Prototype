# Story 5.6: Reproducible Adversarial Behavior with Seeding

**Epic:** Epic 5 - Adversary Framework
**Week:** Weeks 10-12

## User Story

As a researcher,
I want reproducible adversarial behavior controlled by seed,
So that I can re-run experiments with identical Byzantine patterns.

## Acceptance Criteria

1. Extend all adversary strategies to accept seed parameter
2. Seeded RNG used for: equivocation targets, withhold timing, delay sampling, drop decisions
3. Same seed produces identical adversarial action sequence
4. Seed management: global seed or per-adversary seeds
5. Reproducibility test: two runs with same seed produce identical adversary logs
6. Unit tests covering: seeded equivocation, seeded delays, determinism
7. Integration test: full BA execution with seeded adversaries reproduces results

## Prerequisites

Stories 2.6, 5.5

## Notes

Ensures reproducibility of adversarial experiments.
