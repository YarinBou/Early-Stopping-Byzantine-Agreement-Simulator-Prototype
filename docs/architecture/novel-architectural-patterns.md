# Novel Architectural Patterns

## Pattern 1: Certificate ∨ Timeout Advancement (CORRECTED)

**Problem:** Rounds must progress when terminal-phase (GDA GRADE_VOTE) reaches n-t messages OR Δ timeout expires.

**Key Correction:** Advancement gated ONLY on terminal phase, not on all subprotocol messages.

**Implementation:**
```python
async def wait_for_advancement(self) -> AdvancementReason:
    """Wait for terminal phase certificate or Δ timeout."""
    certificate_task = asyncio.create_task(
        self.certificate_tracker.wait_for_terminal_certificate(n, t)
    )
    timeout_task = asyncio.create_task(asyncio.sleep(self.delta))

    done, pending = await asyncio.wait(
        [certificate_task, timeout_task],
        return_when=asyncio.FIRST_COMPLETED
    )

    for task in pending:
        task.cancel()  # Always cancel pending

    if certificate_task in done:
        return AdvancementReason.CERTIFICATE
    else:
        return AdvancementReason.TIMEOUT
```

**Guarantees:**
- **Liveness:** Timeout prevents deadlock
- **Early-stopping:** Certificate enables (1+ε)f termination
- **Evidence:** Advancement reason recorded

---

## Pattern 2: Round Firewall Enforcement

**Problem:** Late messages (round r arriving in round r+1) must be logged but NEVER mutate state.

**Implementation:**
```python
class RoundFirewall:
    def check_message(self, message: Message) -> FirewallResult:
        if message.round < self.current_round:
            return FirewallResult.LATE_AUDIT_ONLY  # Log, no mutation
        if message.round == self.current_round and not self.round_locked:
            return FirewallResult.ACCEPT  # Safe to process
        return FirewallResult.REJECT

    def advance_round(self):
        self.round_locked = True  # Lock before carryover resolution
        # Resolve carryover here
        self.current_round += 1
        self.round_locked = False
```

**Guarantees:**
- **Round firewall:** Late messages never mutate previous round state
- **Auditability:** Late messages logged with metadata
- **Fail-fast:** Assertion fires on violation attempt

---

## Pattern 3: FSM-Based Protocol Architecture

**Problem:** CoD, GDA, PoP need consistent multi-phase pattern with threshold transitions.

**Base Pattern:**
```python
class ProtocolFSM(ABC):
    def __init__(self, n: int, t: int, node_id: int):
        self.n, self.t, self.node_id = n, t, node_id
        self.current_phase = self.initial_phase()
        self.messages: Dict[Phase, List[Message]] = defaultdict(list)

    @abstractmethod
    def initial_phase(self) -> Phase: pass

    @abstractmethod
    def process_message(self, msg: Message) -> bool: pass

    @abstractmethod
    def check_transition(self) -> Optional[Phase]: pass

    @abstractmethod
    def is_terminal(self) -> bool: pass

    @abstractmethod
    def get_output(self) -> Optional[ProtocolOutput]: pass

    def has_threshold(self, phase: Phase, threshold: int) -> bool:
        senders = {msg.sender_id for msg in self.messages[phase]}
        return len(senders) >= threshold
```

**CoD Example:**
- SEND → ECHO (n-t threshold)
- ECHO → READY (n-t ECHO or t+1 READY)
- READY terminal (n-t threshold)

---

## Pattern 4: BA Controller Orchestration (CORRECTED)

**Problem:** Orchestrate PoP → CoD → GDA, detect grade-2 for early stopping, manage carryover.

**Key Corrections:**
1. **Deterministic fallback** after CoD detect-set (no arbitrary defaults)
2. **DECIDE broadcast** for convergence
3. **Barrier certificate** from terminal phase only

**Critical Flow:**
```python
async def execute_round(self, r: int):
    # 1) Lite PoP
    pop_out = await self.run_lite_pop(r)

    # 2) CoD
    cod_out = await self.run_cod(r, self.current_value)
    if cod_out.meta["type"] == "detect_set":
        candidate = self._select_candidate_deterministic(self.viable_values)
    else:
        candidate = cod_out.value

    # 3) GDA
    gda_out = await self.run_gda(r, candidate)
    grade = gda_out.meta["grade"]
    terminal_cert = gda_out.certificate  # From GRADE_VOTE phase

    # Decision logic
    if grade == 2:
        self.decide(gda_out.value, r, terminal_cert)
        self._broadcast_decide(gda_out.value, r)
        return

    # Prepare carryover (sealed before advance)
    self._update_viable_values(gda_out.value, grade)
    self.round_state = self._compute_carryover(gda_out, terminal_cert)

    # Advance only on terminal certificate ∨ timeout
    adv = await self._advance_round_or_timeout(r)
    self.evidence_store.record_transition(r, adv, self.round_state)
```

**Guarantees:**
- **Early-stopping:** Grade-2 triggers immediate decision
- **Safety:** Deterministic candidate selection prevents divergence
- **Liveness:** Timeout-based fallback
- **Auditability:** Complete evidence trail

---
