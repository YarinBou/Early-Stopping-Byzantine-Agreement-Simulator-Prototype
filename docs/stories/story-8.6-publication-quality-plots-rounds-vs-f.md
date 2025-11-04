# Story 8.6: Publication-Quality Plots - Rounds vs. f

**Epic:** Epic 8 - Experiment Infrastructure & Visualization
**Week:** Weeks 15-18

## User Story

As a researcher,
I want clean plots showing rounds to decision vs. fault count f,
So that I can visually demonstrate early-stopping advantage.

## Acceptance Criteria

1. Create `visualization.py` module with matplotlib plotting functions
2. `plot_rounds_vs_f(results: Statistics, output_path: str)` function
3. Line plot: x-axis = f (fault count), y-axis = rounds to decision
4. Multiple lines: early-stopping (experimental), classical baseline, theoretical (1+ε)f curve
5. Error bars: standard deviation or 95% CI
6. Plot styling: labeled axes, legend, title, grid
7. Export formats: PNG (raster), PDF (vector for publications)
8. Unit tests covering: plot generation (no crashes)
9. Integration test: produces publication-ready plot from real experimental data

## Prerequisites

Story 8.5

## Notes

Core visualization for demonstrating early-stopping advantage.
