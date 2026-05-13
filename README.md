# green-machine-mini

An educational toy model of the **Green Machine** photonic interconnect architecture for distributed modular quantum computing.

## What This Is

This project models the **communication/interconnect layer** between heterogeneous quantum hardware modules. It does **not** simulate trapped-ion, NV-center, or Rydberg-atom physics. Those hardware backends are intentionally owned elsewhere. This repository owns only what happens *between* them: the photonic channel that carries entanglement from module to module.

The Green Machine is a time-multiplexed linear optical network. A single spatial photonic mode is reused across many time bins, with Mach-Zehnder Interferometers (MZIs) routing and interfering photons to generate, route, and fuse entanglement between physically separated quantum processors.

## What This Is Not

- Not a production quantum simulator
- Not a hardware physics engine
- Not a replacement for tools like QuTiP, Qiskit, or CasOptAx
- Not an official implementation of either paper listed below

## Project Structure

```
src/green_machine_mini/
├── modules/          # Placeholder external hardware endpoints (no physics here)
├── interconnect/     # Green Machine: MZIs, time bins, interconnect logic
├── protocols/        # Boosted Bell-state measurement
└── qec/              # Distributed logical qubit encoding (W-code placeholder)
```

## Setup

```bash
# Clone and enter the repo
git clone <repo-url>
cd green-machine-mini

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

## Run the Demo

```bash
python experiments/run_skeleton_demo.py
```

## Run Tests

```bash
pytest
```

## Read the Docs

Start with [`docs/01_project_concept.md`](docs/01_project_concept.md) for the conceptual overview, then proceed in order.

## Ownership Boundary

Hardware-specific qubit preparation for trapped-ion, NV-center, and Rydberg modules is owned by a separate engineer and is entirely outside this repo. The `QuantumHardwareModule` classes here are opaque external endpoint placeholders — they contain no hardware physics. This repo owns only what happens *between* modules: the photonic channel and the protocols that run on it.

| Layer | Owner |
|---|---|
| Trapped-ion qubit preparation | External (separate engineer) |
| NV-center qubit preparation | External (separate engineer) |
| Rydberg qubit preparation | External (separate engineer) |
| Photonic interconnect | This repo |
| Boosted BSM | This repo |
| Entanglement routing | This repo |
| Distributed logical qubit encoding | This repo |

## Research Attribution

This project is an educational/research toy model inspired by the following papers. It is **not** an official implementation of either.

**Green Machine architecture**
Jasvith Raj Basani, Chaohan Cui, Jack Postlewaite, Edo Waks, Saikat Guha.
*"Hardware-Efficient Universal Linear Transformations for Optical Modes in the Synthetic Time Dimension."*
Inspiration: time-bin photonic interconnect, recursive MZI architecture, boosted Bell-state measurement benchmark.

**Distributed approximate quantum error correction**
Connor Clayton and Bruno Avritzer.
*"Distributed Quantum Error Correction with Permutation-Invariant Approximate Codes."*
Inspiration: distributed approximate QEC framing, W-state/permutation-invariant code intuition, logical qubit information distributed across multiple processors.
