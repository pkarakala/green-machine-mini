# 02 — The Green Machine Interconnect

## The core idea: time-multiplexing

Connecting N quantum modules naively would require N separate photonic channels — one fiber per
module. The Green Machine takes a different approach: **a single spatial optical mode is reused
across N time slots**.

A photon from module A arrives at time t=0. A photon from module B arrives at t=1. A photon from
module C arrives at t=2. They all travel through the *same* fiber but at different times. A
switchable delay loop holds each photon long enough for the next one to arrive, so they can be
made to interfere with one another.

This is called **time-bin multiplexing** and is the key hardware-efficiency trick of the Green
Machine.

```
Time:      t=0       t=1       t=2       t=3  ...
           │         │         │         │
module A ──►         │         │         │
           │         │         │         │
           ▼         ▼         ▼         ▼
fiber: ════════════════════════════════════════► MZI mesh → detectors
```

---

## Mach-Zehnder Interferometers (MZIs)

The basic optical element in the Green Machine is the **Mach-Zehnder Interferometer (MZI)**.
An MZI is a 2-input, 2-output device that splits an incoming optical field on a beam splitter,
applies a phase shift to one arm, and recombines on a second beam splitter.

```
         ┌────────┐  φ  ┌────────┐
in_0 ───►│  BS1   ├──●──┤  BS2   ├──► out_0
         │        │     │        │
in_1 ───►│ (50/50)├─────┤ (50/50)├──► out_1
         └────────┘     └────────┘
```

The action of a single MZI on its two input modes is described by a 2×2 unitary matrix:

```
U(θ, φ) = [ e^{iφ} cos θ    -sin θ ]
          [ e^{iφ} sin θ     cos θ ]
```

where θ controls how much light is split between the two arms, and φ is the differential phase.

By chaining many MZIs in a rectangular or triangular mesh, you can implement an *arbitrary*
N×N unitary transformation on N optical modes. This is how the Green Machine routes photons
between time bins.

**What is simplified here:**
- Real MZIs have imperfections, loss, and bandwidth limitations.
- We treat every MZI as perfectly lossless and monochromatic.

---

## The full interconnect picture

```
Hardware modules          Green Machine interconnect           Detectors
─────────────────         ─────────────────────────           ─────────

trapped_ion  ──────►  [bin 0] ──┐
                                │
nv_center    ──────►  [bin 2] ──┼──  MZI mesh  ──────────►  D0, D1, D2 ...
                                │   (routing +
rydberg      ──────►  [bin 5] ──┘    interference)

            free bins: 1, 3, 4, 6, 7 — available for auxiliary photons
                       used in the boosted BSM protocol
```

The interconnect:
1. Accepts one photon per module, arriving at its assigned time-bin slot.
2. Routes photons through the MZI mesh, causing them to interfere.
3. Records which detectors click — the click pattern encodes the Bell-state measurement outcome.
4. Sends a classical correction signal back to the relevant hardware modules.

---

## What is physically accurate vs. intentionally simplified?

| Aspect | Status |
|---|---|
| Time-bin multiplexing concept | Accurate |
| MZI unitary matrix | Accurate |
| Arbitrary NxN unitary from MZI mesh | Accurate (theorem) |
| Actual routing angles (θ, φ) for a specific protocol | **Placeholder** |
| Photon loss in the delay loop | **Ignored** |
| Detector efficiency and dark counts | **Ignored** |
