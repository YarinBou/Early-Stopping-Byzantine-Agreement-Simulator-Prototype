# Complete Project Structure

```
final-project-code/
├── src/ba_simulator/              # Main package (src/ layout)
│   ├── transport/                 # Epic 1: Messages, crypto, validation
│   │   ├── message.py            # Message dataclass
│   │   ├── serialization.py      # MessageSerializer interface
│   │   ├── crypto.py             # Ed25519 NodeKeys
│   │   └── validation.py         # MessageValidator
│   ├── scheduling/                # Epic 2: Round scheduler, timing
│   │   ├── scheduler.py          # RoundScheduler
│   │   ├── certificate_tracker.py
│   │   ├── determinism.py        # Hierarchical seeding
│   │   ├── clocks.py             # Dual clocks
│   │   └── firewall.py           # Round firewall
│   ├── protocols/                 # Epic 3: CoD, GDA, PoP FSMs
│   │   ├── protocol_fsm.py
│   │   ├── cod.py
│   │   ├── gda.py
│   │   └── lite_pop.py
│   ├── controller/                # Epic 4: BA controller
│   │   ├── ba_controller.py
│   │   └── assertions.py
│   ├── adversaries/               # Epic 5: Adversary models
│   │   ├── adversary.py
│   │   ├── equivocator.py
│   │   ├── withholder.py
│   │   ├── delay_drop.py
│   │   └── composition.py
│   ├── validation/                # Epic 6: Evidence store
│   │   └── evidence_store.py
│   ├── baselines/                 # Epic 7: Classical BA
│   │   └── classical_ba.py
│   └── experiments/               # Epic 8: Harness, metrics, plots
│       ├── config.py
│       ├── harness.py
│       ├── metrics.py
│       ├── statistics.py
│       └── visualization.py
├── tests/                         # Mirrors src/ structure
│   ├── unit/
│   ├── integration/
│   ├── property/
│   └── conftest.py
├── experiments/configs/           # YAML experiment definitions
├── experiments/results/           # CSV outputs
├── experiments/plots/             # PNG/PDF visualizations
├── docs/
├── requirements.txt
├── setup.py
└── README.md
```

---
