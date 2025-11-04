# Performance Considerations

## Research Performance Targets (NFR-3.3)

**Acceptable for MVP:**
- Single run (n=31): < 5 minutes
- Full campaign (500-1000 runs): < 24 hours
- Memory: < 8GB RAM
- Storage: < 1GB for all results

**Performance is NOT a primary concern** (NFR-3.2):
- Logging overhead acceptable
- Detailed tracing enabled
- Research correctness > execution speed

## Optimization Strategy

**Phase 1 (MVP):** Correctness only
- No premature optimization
- All logging/instrumentation enabled
- In-memory evidence store

**Phase 2 (Post-thesis):**
- Signature batching
- Message compression (CBOR)
- Distributed multi-machine execution

## Measurement Approach

**Dual clocks enable:**
- Protocol timing (simulated) → deterministic
- Performance measurement (wall-clock) → actual cost
- Separation of concerns

**Metrics tracked:**
- Rounds to decision (primary research metric)
- Total messages
- Cryptographic operations (sign/verify counts)
- Wall-clock time per run

---
