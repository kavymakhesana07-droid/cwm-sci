# Causal World Model for Scientific Discovery (CWM-Sci)

A foundation model that learns **causal laws** from scientific literature and observational data with formal **do-calculus proofs**.

> **Status**: v0.1.0 - Early alpha (core causal engine implemented)

---

## Overview

CWM-Sci is a **first-of-its-kind** foundation model that learns **causal laws** (not just correlations) from scientific literature and observational data, with **formal do-calculus proofs** for every causal claim.

### Key Innovations

| Capability | Traditional ML | CWM-Sci |
|------------|----------------|---------|
| **Learns** | Correlations | **Causal laws** (do-calculus proofs) |
| **Answers** | "What correlates with Y?" | **"What causes Y? (proof)"** |
| **Counterfactuals** | Heuristic | **do-calculus proofs** |
| **Interventions** | Heuristic | **do-calculus planning** |
| **Transfer** | Poor (correlations don't transfer) | **Causal graphs transfer** |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 CWM-Sci Architecture                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Causal       │───▶│ Do-Calculus  │───▶│ Counterfactual  │
│  │ Discovery    │    │ Engine       │    │ Planner         │
│  └──────────────┘    └──────────────┘    └─────────────────┘  │
│         │                   │                    │             │
│         ▼                   ▼                    ▼             │
│  ┌──────────────────────────────────────────────────────┐     │
│  │              Causal Graph Engine                      │     │
│  │  • d-separation  • Markov blankets  • Path finding   │     │
│  └──────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/kavymakhesana07-droid/cwm-sci.git
cd cwm-sci

# Install dependencies
pip install -e ".[dev,ml]"

# Or with pip
pip install -e .
```

### Optional: ML Dependencies (for training)
```bash
pip install -e ".[ml]"
```

---

## Quick Start

### 1. Causal Discovery from Data

```bash
# Discover causal structure from CSV data
cwm-sci discover data.csv --algorithm pc --output graph.graphml

# With domain knowledge
cwm-sci discover data.csv --algorithm ges --significance 0.01
```

### 2. Counterfactual Reasoning

```bash
# Ask counterfactual questions
cwm-sci reason "What if we block IP 192.168.1.100?"
```

### 3. Train Models

```bash
# Train LSTM autoencoder (deep path)
cwm-sci train --data data/train.json --output /models/lstm_ae --epochs 50

# Train XGBoost supervised detector
cwm-sci train --data data/labeled.json --model xgboost --output /models/xgboost
```

### 4. Start API Server

```bash
cwm-sci serve --host 0.0.0.0 --port 8080
```

Then query via REST API:
```bash
curl -X POST http://localhost:8080/api/v1/counterfactual \
  -H "Content-Type: application/json" \
  -d '{"intervention": {"block_ip": "192.168.1.100"}, "outcome": "compromise", "evidence": {}}'
```

---

## Python API

```python
import asyncio
import pandas as pd
from cwm_sci.causal.discovery import CausalDiscoveryEngine, DiscoveryConfig
from cwm_sci.engine.calculus import DoCalculusEngine, CounterfactualQuery
from cwm_sci.engine.graph import CausalGraphEngine

async def main():
    # 1. Causal Discovery
    engine = CausalDiscoveryEngine(DiscoveryConfig(algorithm="pc"))
    data = pd.read_csv("data.csv")
    graph = await engine.discover(data, algorithm="pc")

    # 2. Counterfactual Reasoning
    engine = DoCalculusEngine(causal_graph)
    result = engine.compute_counterfactual(
        outcome="compromise",
        intervention={"block_ip": "192.168.1.100"},
        evidence={"src_ip": "192.168.1.100"}
    )
    print(f"P(compromise | do(block)) = {result.probability:.3f}")

    # Counterfactual planning
    from cwm_sci.engine.calculus import CounterfactualPlanner
    planner = CounterfactualPlanner(calculus_engine)
    plan = planner.plan_intervention(
        target_outcome="compromise",
        desired_probability=0.01,
        available_actions=["block_ip", "patch_vuln", "isolate_host"]
    )
```

---

## Architecture

```
cwm-sci/
├── cwm_sci/
│   ├── causal/
│   │   ├── discovery.py      # Causal discovery (PC, GES, NOTEARS)
│   │   ├── graph.py          # Causal graph operations
│   │   └── laws.py           # Causal law extraction
│   ├── engine/
│   │   ├── calculus.py       # Do-calculus engine
│   │   ├── graph.py          # Graph operations
│   │   └── planner.py        # Counterfactual planner
│   ├── models.py             # Data models (CausalLaw, ProofTree, etc.)
│   ├── api.py                # FastAPI REST API
│   ├── cli.py                # CLI entry point
│   └── models.py             # Data models (Pydantic + dataclasses)
├── tests/
│   ├── unit/
│   └── integration/
├── examples/
├── docs/
├── scripts/
└── pyproject.toml
```

---

## Core Capabilities

### 1. Causal Discovery
- **PC Algorithm** - Constraint-based discovery
- **GES** - Greedy Equivalence Search
- **NOTEARS** - Continuous optimization
- Domain knowledge integration

### 2. Do-Calculus Engine
- **Rule 1**: Insertion/deletion of observations
- **Rule 2**: Action/observation exchange
- **Rule 3**: Insertion/deletion of actions
- Counterfactual queries: `P(Y | do(X), Z)`
- Counterfactual planning

### 3. Causal Graph Operations
- d-separation queries
- Markov blanket / boundary
- Backdoor path detection
- Adjustment set finding
- Graph validation & metrics

### 4. Causal Laws & Proofs
- Causal law extraction with formal proofs
- Do-calculus proof trees
- Counterfactual query answering
- Production readiness checks

---

## Quick Demo

```bash
# 1. Install
pip install -e ".[dev]"

# 2. Run discovery on sample data
cwm-sci discover data/sample.csv --algorithm pc --output graph.graphml

# 2. Query counterfactuals
cwm-sci reason "What if we block IP 192.168.1.100?"
```

---

## Requirements

- Python 3.11+
- See `pyproject.toml` for full dependencies

### Optional ML Dependencies
```bash
pip install -e ".[ml]"
# Installs: torch, lightning, dowhy, econml, causalgraphicalmodels
```

---

## Testing

```bash
# Unit tests
pytest tests/unit -v

# Integration tests (require services)
pytest tests/integration -v

# All tests
pytest -v
```

---

## License

MIT License - See [LICENSE](LICENSE)

---

## Citation

```bibtex
@software{cwm_sci,
  author = {Kavy Makhesana},
  title = {Causal World Model for Scientific Discovery (CWM-Sci)},
  version = {0.1.0},
  year = {2026},
  url = {https://github.com/kavymakhesana07-droid/cwm-sci}
}
```

---

## License

MIT License - See [LICENSE](LICENSE) for details.