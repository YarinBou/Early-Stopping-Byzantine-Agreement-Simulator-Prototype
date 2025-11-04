# Implementation Patterns (Agent Consistency)

## 1. Naming Patterns

**Module/File:** `snake_case` (e.g., `ba_controller.py`)
**Classes:** `PascalCase` (e.g., `BAController`, `CoD`, `GDA`)
**Functions/Methods:** `snake_case` (e.g., `process_message()`)
**Boolean methods:** Prefix `is_`, `has_`, `can_`, `should_`
**Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_ROUNDS`)
**Protocol params:** `n`, `t`, `f`, `delta` (standard notation)
**Message fields:** Exact from PRD: `ssid`, `round`, `protocol_id`, `phase`, `sender_id`, `value`, `digest`, `aux`, `signature`

**Enforcement:** All agents MUST use these exact conventions.

---

## 2. Structure Patterns

**Import organization** (3 groups):
```python
# Standard library
import asyncio
from dataclasses import dataclass

# Third-party
import structlog

# Local
from ba_simulator.transport.message import Message
```

**FSM state attributes:**
- `self.current_phase: Phase`
- `self.messages: Dict[Phase, List[Message]]`
- `self.thresholds_reached: Set[Phase]`

**Evidence store collections:**
- `barrier_certificates: Dict[int, BarrierCertificate]`
- `transition_records: Dict[int, TransitionRecord]`
- `decision_packages: Optional[DecisionPackage]`

---

## 3. Format Patterns

**JSON serialization:** `sort_keys=True`, base64 for binary
**Structured logs:** `log.info("event_name", field=value, timestamp=time.time())`
**CSV columns (experiments):** `n`, `t`, `f`, `adversary_type`, `run_id`, `rounds`, `messages`, `crypto_ops`, `decision_value`, `wall_time`
**YAML config:** `snake_case` keys

---

## 4. Communication Patterns

**Broadcast:** `await scheduler.broadcast(message)` (never direct node-to-node)
**Collection:** `await scheduler.collect_messages(round, protocol, phase, threshold, timeout=delta)` (always provide timeout)
**Asyncio coordination:** Use `asyncio.wait(FIRST_COMPLETED)`, always cancel pending

---

## 5. Lifecycle Patterns

**Round lifecycle:**
1. `round_start(r)`
2. Execute PoP → CoD → GDA
3. Check decision (grade-2)
4. `wait_for_advancement()` (terminal cert ∨ timeout)
5. `record_transition()`
6. `advance_round()`

**FSM lifecycle:**
1. Initialize in `initial_phase()`
2. `process_message()` → accumulate
3. `check_transition()` → phase change
4. Loop until `is_terminal()` True
5. `get_output()` → ProtocolOutput

**Error categories:**
- **FATAL:** Raise immediately (Agreement/Validity violations, round firewall breaches)
- **EXPECTED:** Log and continue (invalid signatures, Byzantine behavior)
- **RECOVERABLE:** Retry/fallback (timeout advancement)

---

## 6. Location Patterns

**Code:** `src/ba_simulator/<epic_module>/`
**Tests:** `tests/unit/test_<epic_module>/`
**Configs:** `experiments/configs/*.yaml`
**Results:** `experiments/results/*.csv`
**Plots:** `experiments/plots/*.png` and `*.pdf`
**Logs:** `logs/ba_simulator_<timestamp>.jsonl`

---

## 7. Consistency Patterns (Cross-Cutting)

**Dual clocks:**
- Simulated: `SimulatedClock.now()` for protocol logic
- Wall-clock: `time.perf_counter()` for performance metrics

**Thresholds:** Always compute, never hardcode
- Strong: `n - t`
- Weak: `t + 1`

**Seeding:** Hierarchical derivation
```python
component_seed = hash((master_seed, component_name, id)) % 2**32
self.rng = random.Random(component_seed)
```

**Hash function:** SHA-256 only (no MD5/SHA-1)

**Property assertions:** Call at every decision, experiment end

---
