# Architecture Decision Records (ADRs)

## ADR-001: src/ Layout vs Flat Layout
**Decision:** src/ layout
**Rationale:** Scientific Python standard, prevents accidental imports, supports future distribution
**Status:** Accepted

## ADR-002: pip vs Poetry vs Conda
**Decision:** pip + requirements.txt
**Rationale:** PRD-specified, simple, pure Python dependencies, easiest for researchers to replicate
**Status:** Accepted

## ADR-003: Evidence Store Persistence
**Decision:** Hybrid (in-memory + checkpoint)
**Rationale:** Best performance during protocol execution, safety via checkpoint, simple JSON export
**Status:** Accepted

## ADR-004: Asyncio Determinism Strategy
**Decision:** Lock-step rounds + seeded delays
**Rationale:** Naturally fits synchronous model, enables reproducibility, realistic network behavior
**Status:** Accepted

## ADR-005: Message Serialization Abstraction
**Decision:** Serializer interface with JSON implementation
**Rationale:** Clean abstraction for future CBOR migration, debuggable MVP, zero performance impact
**Status:** Accepted

## ADR-006: Configuration Split
**Decision:** Python dataclasses for code config, YAML for experiments
**Rationale:** Type safety for code, flexibility for experiments, clear separation of concerns
**Status:** Accepted

## ADR-007: Testing Structure
**Decision:** Standard pytest structure mirroring src/
**Rationale:** Clear separation, pytest discovery, scalable to 49 stories, standard practice
**Status:** Accepted

## ADR-008: Structured Logging
**Decision:** structlog for JSON structured logs
**Rationale:** Machine-parseable, research analysis-friendly, queryable logs for audit
**Status:** Accepted

## ADR-009: Error Handling Strategy
**Decision:** Hybrid (fail-fast for bugs, graceful for Byzantine)
**Rationale:** Zero tolerance for correctness violations, handle expected adversarial behavior
**Status:** Accepted

## ADR-010: Dual Clock Timing
**Decision:** Simulated clock (protocol) + wall-clock (performance)
**Rationale:** Deterministic protocol logic, real performance measurement, satisfies NFR-2.1 and Epic 8 requirements
**Status:** Accepted

## ADR-011: Hierarchical RNG Seeding
**Decision:** Master seed derives component seeds deterministically
**Rationale:** Independent components, reproducible yet composable, order-independent
**Status:** Accepted

## ADR-012: Dataclasses for Data Models
**Decision:** Python 3.10+ dataclasses (no Pydantic)
**Rationale:** Built-in, type safety, no external dependencies, clean integration
**Status:** Accepted

---
