# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

`green-machine-mini` is an educational/research toy model of the **Green Machine photonic interconnect** for distributed modular quantum computing. It models the **communication layer only** — how photons carry entanglement between heterogeneous quantum hardware modules (trapped-ion, NV-center, Rydberg). Hardware-specific qubit preparation is intentionally out of scope and owned by a separate engineer.

This is **not** an official implementation of either paper it draws from. It exists to build intuition and support future experiments.

## Research attribution

**Paper 1 — Green Machine architecture:**
Jasvith Raj Basani, Chaohan Cui, Jack Postlewaite, Edo Waks, Saikat Guha.
*"Hardware-Efficient Universal Linear Transformations for Optical Modes in the Synthetic Time Dimension."*
This repo is inspired by the time-bin photonic interconnect, recursive MZI architecture, and boosted Bell-state measurement benchmark described in this paper.

**Paper 2 — Distributed approximate QEC:**
Connor Clayton and Bruno Avritzer.
*"Distributed Quantum Error Correction with Permutation-Invariant Approximate Codes."*
This repo is inspired by the distributed approximate QEC framing, W-state/permutation-invariant code intuition, and the idea that logical qubit information can be distributed across multiple processors.

## Ownership boundary

| Layer | Owner |
|---|---|
| Trapped-ion qubit preparation | External (separate engineer) |
| NV-center qubit preparation | External (separate engineer) |
| Rydberg qubit preparation | External (separate engineer) |
| Photonic interconnect | This repo |
| Boosted BSM | This repo |
| Entanglement routing | This repo |
| Distributed logical qubit encoding | This repo |

`modules/module.py` contains zero physics. Its `emit_photon()` method returns a `PhotonEmission` token; hardware logic lives entirely outside this repo.

## Commands

```bash
# Install (editable, with dev dependencies)
pip install -e ".[dev]"

# Run demo
python experiments/run_skeleton_demo.py

# Run all tests
pytest

# Run a single test
pytest tests/test_imports.py::TestMZI::test_unitarity -v
```

## Architecture

```
src/green_machine_mini/
├── modules/          # QuantumHardwareModule — opaque external hardware endpoints, no physics
├── interconnect/
│   ├── mzi.py        # MZI: 2×2 unitary building block (theta, phi parameterization)
│   ├── time_bins.py  # TimeBinRegister: tracks which module owns which time-bin slot
│   └── green_machine.py  # GreenMachineInterconnect: top-level object; glues everything
├── protocols/
│   └── boosted_bsm.py    # BoostedBSM: placeholder BSM with auxiliary photon boost logic
└── qec/
    └── distributed_w_code.py  # DistributedLogicalQubit: W-state distributed encoding
```

**Key object relationships:**
- `GreenMachineInterconnect` owns a `TimeBinRegister` and a list of `MZI` elements.
- `QuantumHardwareModule` instances are registered with the interconnect via `register_module(module, time_bin_index)`, which assigns a slot in the `TimeBinRegister` and calls `module._assign_time_bin()`.
- `BoostedBSM` and `DistributedLogicalQubit` are protocol-level objects used independently on top of the interconnect.

**Ownership boundary enforced by design:** The hardware module classes are opaque external endpoint placeholders. See the ownership boundary table above.

## Physics placeholders

All math in this skeleton is either physically grounded (MZI unitary, 50% BSM limit) or an explicit placeholder. See the `docs/` folder for what is accurate vs. deferred. The boosted BSM success probability formula `1 − (1/2)^(N+1)` is approximate; real values require a full scattering-matrix calculation.

## Neighboring reference

`CasOptAx` at `../CasOptAx` is a full quantum photonic simulator (JAX-based) used as research inspiration. Do not import it here.
