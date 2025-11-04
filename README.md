# Byzantine Agreement Simulator

A Python implementation of Byzantine Agreement protocols with early stopping mechanisms, designed for research and experimental analysis.

## Project Overview

This simulator implements and compares Byzantine Agreement protocols, focusing on early-stopping mechanisms based on graded consensus. The project provides:

- **Core Protocol Implementation**: Message transport layer with cryptographic signing and validation
- **Round Scheduling**: Asynchronous round-based execution with timeout enforcement
- **Multiple Protocol Variants**: COD (Consistent One-shot Disseminate), GDA (Graded Disseminate and Agree), and classical BA protocols
- **Byzantine Adversary Modeling**: Configurable adversarial behaviors for testing protocol resilience
- **Experimental Framework**: Batch experiment execution with statistical analysis and visualization

## Requirements

- Python 3.10 or higher
- Virtual environment recommended for dependency isolation

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd final-project-code
```

### 2. Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

Run the test suite to verify everything is set up correctly:

```bash
pytest
```

## Project Structure

```
final-project-code/
├── src/
│   └── ba_simulator/          # Main package
│       ├── transport/          # Message handling and cryptography
│       ├── scheduling/         # Round scheduling and timing
│       ├── protocols/          # Protocol implementations (COD, GDA, etc.)
│       ├── controller/         # BA controller orchestration
│       ├── adversaries/        # Byzantine adversary strategies
│       ├── validation/         # Evidence collection and validation
│       ├── baselines/          # Classical protocol baselines
│       └── experiments/        # Experimental harness and analysis
├── tests/
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── property/               # Property-based tests
├── experiments/
│   └── results/                # Experimental results and data
└── docs/                       # Documentation
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/ba_simulator --cov-report=html

# Run specific test categories
pytest tests/unit
pytest tests/integration
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## Documentation

See the `docs/` directory for:
- Architecture documentation
- Technical specifications
- Protocol descriptions
- Experimental methodology

## License

[Add your license here]

## Contributors

[Add contributors here]
