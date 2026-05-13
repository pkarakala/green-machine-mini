"""
Skeleton demo: Green Machine Interconnect with three heterogeneous hardware modules.

This script shows:
  1. Creating placeholder hardware module endpoints.
  2. Wiring them into a Green Machine interconnect via time-bin slots.
  3. Running a placeholder boosted Bell-state measurement between two modules.
  4. Tracking a distributed logical qubit across all three modules.
  5. Simulating partial module failure and observing graceful degradation.

None of the hardware physics is simulated — this is purely an interconnect-layer demo.
"""

from green_machine_mini.interconnect.green_machine import GreenMachineInterconnect
from green_machine_mini.modules.module import ModuleType, QuantumHardwareModule
from green_machine_mini.protocols.boosted_bsm import BoostedBSM
from green_machine_mini.qec.distributed_w_code import DistributedLogicalQubit


def main() -> None:
    print("\n" + "=" * 60)
    print("  Green Machine Mini — Skeleton Demo")
    print("=" * 60 + "\n")

    # ------------------------------------------------------------------
    # Step 1: Create placeholder hardware module endpoints.
    #
    # Each module represents an external quantum processor. We do not
    # implement any of their internal physics here.
    # ------------------------------------------------------------------
    print("Step 1: Creating placeholder hardware module endpoints...\n")

    trapped_ion = QuantumHardwareModule(
        name="trapped_ion",
        module_type=ModuleType.TRAPPED_ION,
    )
    nv_center = QuantumHardwareModule(
        name="nv_center",
        module_type=ModuleType.NV_CENTER,
    )
    rydberg = QuantumHardwareModule(
        name="rydberg",
        module_type=ModuleType.RYDBERG,
    )

    print(f"  {trapped_ion}")
    print(f"  {nv_center}")
    print(f"  {rydberg}")
    print()

    # ------------------------------------------------------------------
    # Step 2: Create the Green Machine interconnect with 8 time-bin modes.
    #
    # Each module will be assigned one time-bin slot. The remaining slots
    # are available for auxiliary photons used in the boosted BSM.
    # ------------------------------------------------------------------
    print("Step 2: Creating Green Machine interconnect with 8 time-bin modes...\n")

    interconnect = GreenMachineInterconnect(n_time_bins=8)
    print(f"  {interconnect}\n")

    # ------------------------------------------------------------------
    # Step 3: Register the hardware modules with the interconnect.
    #
    # Each module is pinned to a specific time-bin slot. The interconnect
    # will use this mapping to route photons correctly.
    # ------------------------------------------------------------------
    print("Step 3: Registering modules with the interconnect...\n")

    interconnect.register_module(trapped_ion, time_bin_index=0)
    interconnect.register_module(nv_center, time_bin_index=2)
    interconnect.register_module(rydberg, time_bin_index=5)

    for mod in interconnect.registered_modules():
        print(f"  {mod}")
    print()

    # ------------------------------------------------------------------
    # Step 4: Each module emits a photon into the interconnect.
    # ------------------------------------------------------------------
    print("Step 4: Hardware modules emitting photons into the interconnect...\n")

    for mod in interconnect.registered_modules():
        emission = mod.emit_photon()
        print(f"  {emission}")
    print()

    # ------------------------------------------------------------------
    # Step 5: Placeholder boosted Bell-state measurement between two modules.
    #
    # The Green Machine boosted BSM uses 2 dual-rail qubits plus 4 ancillary
    # single-photon modes, giving an ideal success probability of 75%.
    # ------------------------------------------------------------------
    print("Step 5: Boosted Bell-state measurement (trapped_ion ↔ nv_center)...\n")

    bsm = BoostedBSM(n_ancilla_modes=4)
    print(f"  Protocol: {bsm}")

    outcome = bsm.attempt_measurement(
        module_a_name="trapped_ion",
        module_b_name="nv_center",
    )
    print(f"  Outcome : {outcome}")
    print()

    # ------------------------------------------------------------------
    # Step 6: Distributed logical qubit across all three modules.
    # ------------------------------------------------------------------
    print("Step 6: Distributed logical qubit across all three modules...\n")

    logical_qubit = DistributedLogicalQubit(
        module_names=["trapped_ion", "nv_center", "rydberg"],
        label="L0",
    )
    print(logical_qubit.status_report())
    print()

    # ------------------------------------------------------------------
    # Step 7: Simulate partial module failure.
    #
    # The nv_center module goes offline. Because the encoding is
    # permutation-invariant, the logical qubit is degraded but not lost.
    # ------------------------------------------------------------------
    print("Step 7: Simulating nv_center module failure...\n")

    logical_qubit.mark_failed("nv_center")
    print(logical_qubit.status_report())
    print()

    # ------------------------------------------------------------------
    # Step 8: Full interconnect summary.
    # ------------------------------------------------------------------
    print("Step 8: Full interconnect summary...\n")
    print(interconnect.summary())


if __name__ == "__main__":
    main()
