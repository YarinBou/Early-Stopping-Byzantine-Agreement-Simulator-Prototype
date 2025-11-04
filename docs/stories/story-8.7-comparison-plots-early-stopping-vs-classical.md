# Story 8.7: Comparison Plots - Early-Stopping vs. Classical

**Epic:** Epic 8 - Experiment Infrastructure & Visualization
**Week:** Weeks 15-18

## User Story

As a researcher,
I want side-by-side comparison plots,
So that I can demonstrate 2-5× round reduction visually.

## Acceptance Criteria

1. Extend visualization with comparison plotting
2. `plot_comparison(early_results, classical_results, output_path)` function
3. Comparison metrics: rounds, messages, crypto operations
4. Bar charts: early-stopping vs. classical side-by-side per (n, f) configuration
5. Percentage improvement annotation: "(X% fewer rounds)"
6. Color coding: early-stopping (green), classical (red)
7. Unit tests covering: comparison plot generation
8. Integration test: visual confirmation early-stopping < classical in low-fault regime

## Prerequisites

Story 8.6

## Notes

Direct visual comparison demonstrating performance advantage.
