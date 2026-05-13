# 04 — Distributed Logical Qubit

## Why distribute a logical qubit?

A single physical qubit — one ion in a trap, one electron spin in an NV center — has two
problems:

1. **Fragility**: One hardware failure destroys the qubit.
2. **Locality**: It is physically stuck inside one module and can only be accessed by that module.

By encoding one **logical qubit** across the physical qubits of *multiple* hardware modules,
we can solve both problems:

- **Fault tolerance**: If one module fails, the other modules still hold enough information
  to recover the logical qubit.
- **Accessibility**: Any module holding part of the encoding can interact with the logical qubit
  without moving it.

This is the core idea of **distributed modular quantum computing**.

---

## The W-state: a natural distributed encoding

The simplest distributed encoding across N modules uses a **W-state**:

```
|W_N⟩ = (|100...0⟩ + |010...0⟩ + ... + |000...1⟩) / √N
```

Here each term represents exactly one module being "excited" (holding the photon or spin-up
state) while all others are in the ground state.

### Loss tolerance

The key property of the W-state is **graceful degradation**:

> If any one module is lost (traced out), the remaining N-1 modules are left in a W_{N-1} state.

No information is catastrophically destroyed. The encoding degrades smoothly. Compare this to
a GHZ state (cat state), where losing one qubit completely destroys the entanglement.

### Example with 3 modules

```
Start:       |W_3⟩ = (|100⟩ + |010⟩ + |001⟩) / √3
             modules: [trapped_ion, nv_center, rydberg]

nv_center fails:
             Remaining = Tr_{nv}(|W_3⟩⟨W_3|) → |W_2⟩ = (|10⟩ + |01⟩) / √2
             modules: [trapped_ion, rydberg]

Logical qubit: degraded but still present. Code distance reduced.
```

---

## Permutation-invariant (PI) codes

W-states are a special case of a broader family called **permutation-invariant codes**.
A PI code is symmetric under any permutation of its physical qubits — swapping which module
holds which qubit does not change the encoded logical state.

This is ideal for modular architectures because:

- Modules can be added or removed without re-encoding the logical qubit from scratch.
- Entanglement can be routed through any path without caring about module order.
- The code does not depend on a fixed connectivity graph.

The price is that PI codes typically have lower code distance than codes that exploit a fixed
topology (like surface codes). The right trade-off depends on the hardware failure rates.

---

## How the Green Machine enables distributed encoding

Creating a W-state across N modules requires entanglement between all N modules. The Green
Machine provides this via the boosted BSM:

1. Each module prepares its local qubit.
2. Each module emits a photon into the Green Machine delay loop.
3. The interconnect performs sequential boosted BSMs between pairs of modules.
4. After enough BSMs, the modules share a W-state (or a higher-quality PI code state).
5. Classical feedforward signals (BSM outcomes) tell each module which Pauli correction to apply.

Step 3–5 are **placeholders** in this skeleton. The actual circuit is future work.

---

## Partial failure is less catastrophic

Under a PI code, the impact of losing K modules out of N is:

- **Code distance** drops from d to d - K (roughly).
- The logical qubit is **still recoverable** as long as enough modules survive.
- There is no sharp cliff where losing one more module suddenly destroys everything.

This is in contrast to a topological code (like a surface code), where losing a line of qubits
along a specific boundary can cut the logical qubit in two.

For a heterogeneous modular system where different hardware types have different failure rates,
this smooth degradation is a significant practical advantage.

---

## What is physically accurate vs. intentionally simplified?

| Aspect | Status |
|---|---|
| W-state definition and structure | Accurate |
| W-state loss-tolerance property | Accurate |
| Permutation-invariant code concept | Accurate |
| PI code distance under partial loss | Accurate (conceptually) |
| W-state preparation circuit via Green Machine | **Placeholder** |
| Pauli correction feedforward protocol | **Placeholder** |
| Specific PI code construction (beyond W-states) | **Future work** |
