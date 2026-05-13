# 01 — Project Concept

## What problem are we solving?

Modern quantum computers are small. A single trapped-ion trap, NV-center device, or Rydberg array
holds tens to hundreds of qubits. This is far fewer than the millions of high-quality qubits
that fault-tolerant quantum computation will eventually require.

The answer is **modular quantum computing**: build many small quantum processors and wire them
together into a larger logical machine. The hard part is the wire.

Classical computers are connected with copper traces and optical fibers that carry billions of
bits per second. Quantum computers must be connected with *entanglement* — a fragile quantum
correlation that cannot simply be copied or amplified. Distributing entanglement between two
physically separated quantum modules requires flying photons.

---

## What is green-machine-mini?

`green-machine-mini` is an educational toy model of the **photonic interconnect layer** between
quantum hardware modules. It models:

- How photons are time-multiplexed through a single optical channel.
- How Mach-Zehnder Interferometers (MZIs) route and interfere those photons.
- How Bell-state measurements (BSMs) create entanglement between two remote modules.
- How a logical qubit can be distributed across multiple modules and survive partial failure.

It does **not** model:

- Trapped-ion gate physics.
- NV-center spin dynamics.
- Rydberg atom interactions.
- Low-level photon loss or noise (everything is idealized).

---

## Ownership boundary

This project is intentionally scoped to the **interconnect layer only**.

```
┌─────────────┐        ┌───────────────────────────────┐        ┌─────────────┐
│  trapped-   │◄──────►│                               │◄──────►│  NV-center  │
│  ion trap   │ photon │   Green Machine Interconnect  │ photon │   device    │
│  (external) │        │        (this repo)            │        │  (external) │
└─────────────┘        │                               │        └─────────────┘
                       │  • time-bin multiplexing      │
┌─────────────┐        │  • MZI mesh routing           │
│  Rydberg    │◄──────►│  • boosted BSM                │
│  array      │ photon │  • entanglement routing       │
│  (external) │        │  • distributed logical qubit  │
└─────────────┘        └───────────────────────────────┘
```

The hardware boxes on the left and right are opaque endpoints. The interconnect does not know
how qubits were prepared inside them.

---

## What is physically accurate vs. intentionally simplified?

| Aspect | Status |
|---|---|
| MZI 2×2 unitary matrix | Physically accurate |
| 50% BSM limit with linear optics | Physically accurate |
| Boosted BSM success probability formula | **Placeholder** |
| W-state loss-tolerance property | Physically accurate conceptually |
| W-state circuit preparation | **Placeholder** |
| Time-bin multiplexing concept | Physically accurate |
| Photon loss and decoherence | **Ignored (idealized)** |

---

## Where to go next

- [02 — Green Machine Interconnect](02_green_machine_interconnect.md): How photons flow through the time-bin channel.
- [03 — Boosted BSM](03_boosted_bsm.md): Why linear optics limits Bell-state measurement to 50% and how to do better.
- [04 — Distributed Logical Qubit](04_distributed_logical_qubit.md): Why distributing a logical qubit across modules is powerful.
