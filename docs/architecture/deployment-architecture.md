# Deployment Architecture

## Single-Machine Simulation (MVP)

**Target environment:**
- Laptop/desktop (8GB+ RAM recommended)
- No distributed infrastructure needed
- No Docker/containers required for MVP

**Execution model:**
- All nodes simulated in single Python process
- Asyncio for event-driven concurrency
- Centralized scheduler coordinates all nodes

**Output locations:**
- Results: `experiments/results/`
- Plots: `experiments/plots/`
- Logs: `logs/`
- Evidence checkpoints: `experiments/results/evidence_*.json`

## Future (Phase 2)

**Multi-machine execution:**
- Docker containers per node
- Real network transport
- Distributed evidence store

---
