# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

`green-machine-mini` is an educational toy model of the **Green Machine photonic interconnect** for distributed modular quantum computing. It models the **communication layer only** — how photons carry entanglement between heterogeneous quantum hardware modules (trapped-ion, NV-center, Rydberg). Hardware-specific qubit preparation is intentionally out of scope and owned externally.

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

**Ownership boundary enforced by design:** `modules/module.py` contains zero physics. Its `emit_photon()` method returns a `PhotonEmission` token; hardware logic lives outside this repo.

## Physics placeholders

All math in this skeleton is either physically grounded (MZI unitary, 50% BSM limit) or an explicit placeholder. See the `docs/` folder for what is accurate vs. deferred. The boosted BSM success probability formula `1 − (1/2)^(N+1)` is approximate; real values require a full scattering-matrix calculation.

## Neighboring reference

`CasOptAx` at `../CasOptAx` is a full quantum photonic simulator (JAX-based) used as research inspiration. Do not import it here.
