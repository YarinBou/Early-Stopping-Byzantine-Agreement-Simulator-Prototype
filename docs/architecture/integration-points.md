# Integration Points

## Protocol Stack Integration

```
BAController
    ↓ orchestrates
LitePoP → CoD → GDA
    ↓ messages via
RoundScheduler
    ↓ validates with
MessageValidator
    ↓ signs with
NodeKeys (Ed25519)
```

## Evidence Flow

```
Protocol completion
    ↓ produces
BarrierCertificate (n-t signatures)
    ↓ stored in
EvidenceStore
    ↓ exported to
JSON/CSV for analysis
```

## Experiment Flow

```
ExperimentConfig (YAML)
    ↓ loaded by
BatchRunner
    ↓ executes
BAController × replications
    ↓ collects
RunMetrics
    ↓ analyzes with
Statistics module
    ↓ visualizes with
Matplotlib
```

---
