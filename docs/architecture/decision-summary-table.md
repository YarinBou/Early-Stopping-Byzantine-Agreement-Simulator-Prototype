# Decision Summary Table

| Category | Decision | Rationale | Affects |
|----------|----------|-----------|---------|
| **Project Structure** | src/ layout | Scientific Python standard, future distribution | All epics |
| **Language** | Python 3.10+ | Type hints, dataclasses, asyncio, research standard | All |
| **Dependency Mgmt** | pip + requirements.txt | Simple, version-locked, PRD-specified | All |
| **Evidence Store** | Hybrid (in-memory + checkpoint) | Performance + safety | Epic 6, 8 |
| **Asyncio** | Lock-step rounds + seeded delays | Deterministic + realistic | Epic 2, 4 |
| **Serialization** | Interface (JSON impl) | Abstraction for CBOR migration | Epic 1 |
| **Configuration** | Python dataclasses + YAML | Type-safe code, flexible experiments | Epic 8 |
| **Testing** | Standard pytest structure | Clear boundaries, scalable | All |
| **Logging** | Structured (structlog) | Machine-parseable for analysis | All |
| **Error Handling** | Hybrid (fail-fast + graceful) | Zero tolerance for bugs, handle Byzantine | All |
| **Time** | Dual clocks | Deterministic protocol + real perf | Epic 2, 8 |
| **RNG** | Hierarchical seeding | Independent components | Epic 2, 5 |
| **Data** | Dataclasses | Type safety, built-in | All |

---
