# Development Environment

## Prerequisites

```bash
# Python 3.10+ required
python3 --version

# Virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

## Setup Commands

```bash
# Clone repository
cd final-project-code

# Install in editable mode
pip install -e .

# Run tests
pytest

# Run experiment
python scripts/run_experiment.py --config experiments/configs/sweep_low_faults.yaml

# Lint and format
black src/ tests/
flake8 src/ tests/
mypy src/
```

## Development Workflow

1. **Create feature branch** per story
2. **Write tests first** (TDD encouraged)
3. **Implement story** following implementation patterns
4. **Run tests** (>80% coverage target)
5. **Format code** (black, flake8)
6. **Commit** with story reference

---
