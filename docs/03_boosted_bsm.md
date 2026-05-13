# 03 — Boosted Bell-State Measurement

## What is a Bell-state measurement?

Two qubits (one from module A, one from module B) can be in a superposition of joint states.
A **Bell-state measurement (BSM)** projects those two qubits onto one of four special states
called Bell states:

```
|Φ+⟩ = (|00⟩ + |11⟩) / √2      ← both same, in phase
|Φ-⟩ = (|00⟩ - |11⟩) / √2      ← both same, out of phase
|Ψ+⟩ = (|01⟩ + |10⟩) / √2      ← opposite, in phase
|Ψ-⟩ = (|01⟩ - |10⟩) / √2      ← opposite, out of phase
```

When two modules each emit one photon into the interconnect and the interconnect performs a BSM,
a successful measurement projects the *remaining* qubits of those two modules into one of these
Bell states — meaning the two modules are now **entangled**. This is the foundation of all
long-distance quantum networking.

---

## Standard BSM: the 50% ideal success cap

A BSM on photonic qubits using only beam splitters and phase shifters (linear optics) can, at
best, distinguish **2 of the 4 Bell states** with certainty. The other 2 remain ambiguous and
must be discarded.

This means:
- **50% of BSM attempts succeed** (Bell state identified → modules become entangled).
- **50% of BSM attempts fail** (outcome ambiguous → photons discarded).

This 50% cap is not a technical limitation that better optics can fix. It is a **mathematical
theorem** (Calsamiglia & Lütkenhaus, 2001) about the information-theoretic structure of linear
maps on Fock states.

In `green-machine-mini`: `BoostedBSM(n_ancilla_modes=0)` returns `ideal_success_probability = 0.50`.

---

## Boosted BSM: 4 ancillary modes push success to 75%

The Green Machine circumvents the 50% limit by supplying **ancillary single-photon modes** from
the time-bin delay loop. The specific configuration used in the Green Machine paper is:

- **2 dual-rail photonic qubits** (the signal photons from two modules)
- **4 ancillary single-photon modes** from the delay loop

These ancilla modes interfere with the signal photons in the MZI mesh before detection, giving
the detectors more information about which Bell state was present. For this 4-mode configuration,
the ideal success probability is **75%**.

In `green-machine-mini`: `BoostedBSM(n_ancilla_modes=4)` (the default) returns
`ideal_success_probability = 0.75`.

| Configuration | Ancilla modes | Ideal success probability |
|---|---|---|
| Standard linear optics | 0 | 50% |
| Green Machine boosted BSM | 4 | **75%** |

---

## What this toy code does and does not compute

**What it returns:** Fixed idealized placeholder probabilities (0.50 or 0.75) based on the
paper's reported results.

**What it does not compute yet:**
- The scattering matrix of the signal + ancilla photon system through the MZI mesh.
- The detector click patterns that correspond to each Bell state.
- The decoding table mapping click patterns to Bell state identifications.

These computations are deferred to future work. The `attempt_measurement()` method returns a
fixed `Φ+` outcome as a placeholder to confirm the interface is wired correctly.

---

## Why does this matter for modular quantum computing?

Every time a BSM fails, both photons are discarded and the modules must re-prepare their
photons and try again. This costs time, and time means decoherence.

By boosting the BSM success probability from 50% to 75%, the Green Machine:
1. Generates entanglement between modules faster.
2. Reduces the number of costly re-preparation rounds.
3. Makes distributed quantum computation practically feasible at larger scales.

---

## What is physically accurate vs. intentionally simplified?

| Aspect | Status |
|---|---|
| 50% linear-optics BSM limit | Physically accurate (theorem) |
| 75% ideal success with 4 ancilla modes | Physically accurate (paper result) |
| Ancilla photon boosting concept | Physically accurate |
| Multi-photon scattering matrix | **Not yet implemented** |
| Click-pattern to Bell-state decoding table | **Not yet implemented** |
| MZI angles for specific boosted circuit | **Placeholder** |

## References

- Ewert & van Loock, PRL 113, 140403 (2014) — near-deterministic BSM with ancilla photons
- Grice, PRA 84, 042331 (2011) — arbitrary BSM success probability with linear optics
- Calsamiglia & Lütkenhaus, Appl. Phys. B 72, 67 (2001) — 50% linear-optics limit theorem
