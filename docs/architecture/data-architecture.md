# Data Architecture

## Core Data Models (Dataclasses)

**Message** (Epic 1):
```python
@dataclass
class Message:
    ssid: str
    round: int
    protocol_id: str
    phase: str
    sender_id: int
    value: Any
    digest: Optional[bytes]
    aux: Dict
    signature: bytes
```

**ProtocolOutput** (Epic 3):
```python
@dataclass
class ProtocolOutput:
    value: Any
    certificate: List[Message]
    metadata: Dict
```

**BarrierCertificate** (Epic 6):
```python
@dataclass
class BarrierCertificate:
    round: int
    phase: str
    messages: List[Message]
    digest: bytes
```

**TransitionRecord** (Epic 6):
```python
@dataclass
class TransitionRecord:
    round: int
    reason: str  # "certificate" | "timeout"
    carryover_digest: bytes
    timestamp: float
```

**ExperimentConfig** (Epic 8):
```python
@dataclass
class ExperimentConfig:
    network_sizes: List[int]
    fault_sweeps: List[int]
    adversary_configs: List[Dict]
    replication_count: int
    delta: float
    master_seed: int
```

**RunMetrics** (Epic 8):
```python
@dataclass
class RunMetrics:
    n: int
    t: int
    f: int
    adversary_type: str
    run_id: int
    rounds: int
    messages: int
    crypto_ops: int
    decision_value: Any
    wall_time: float
```

---
