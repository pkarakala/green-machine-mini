"""
Green Machine Interconnect — top-level photonic communication layer.

The Green Machine is a time-multiplexed, delay-loop linear optical network that
connects heterogeneous quantum hardware modules via photons. It is the physical
substrate for:

  1. Module-to-module photon routing
  2. Boosted Bell-state measurement (entanglement generation)
  3. Entanglement routing and swapping
  4. Future: entanglement fusion for logical qubit construction

This file is the main entry point for the interconnect layer. It glues together
the time-bin register, MZI mesh, boosted-BSM protocol, and distributed logical
qubit tracking into a single object that experiments can drive.

Physical accuracy note
----------------------
The GreenMachineInterconnect class is a *conceptual skeleton*. It tracks module
registrations and time-bin allocations accurately, but the actual unitary evolution
(photon routing through the MZI mesh) and measurement simulation are placeholders.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from green_machine_mini.interconnect.mzi import MZI
from green_machine_mini.interconnect.time_bins import TimeBinRegister
from green_machine_mini.modules.module import QuantumHardwareModule

if TYPE_CHECKING:
    pass


class GreenMachineInterconnect:
    """
    The Green Machine photonic interconnect.

    Manages a pool of time-bin modes and the hardware modules connected to them.
    Provides routing, Bell-state measurement, and entanglement-distribution interfaces
    (mostly as conceptual placeholders in this skeleton).

    Parameters
    ----------
    n_time_bins:
        Number of time-bin slots in the optical channel. Each registered module
        occupies exactly one slot.
    """

    def __init__(self, n_time_bins: int) -> None:
        if n_time_bins < 2:
            raise ValueError("Need at least 2 time bins to perform a Bell-state measurement.")
        self.n_time_bins = n_time_bins
        self._register = TimeBinRegister(n_time_bins)
        self._modules: dict[str, QuantumHardwareModule] = {}

        # Placeholder MZI mesh: one MZI per adjacent pair of time bins.
        # In a real Green Machine, the mesh reconfigures between photon arrivals.
        self._mzi_mesh: list[MZI] = [
            MZI(theta=0.0, phi=0.0) for _ in range(n_time_bins - 1)
        ]

    # ------------------------------------------------------------------
    # Module registration
    # ------------------------------------------------------------------

    def register_module(
        self,
        module: QuantumHardwareModule,
        time_bin_index: int,
    ) -> None:
        """
        Register an external hardware module on a specific time-bin slot.

        Each module occupies exactly one time-bin slot. The slot must be free.

        Parameters
        ----------
        module:
            The hardware endpoint to register.
        time_bin_index:
            The time-bin slot to assign this module to.

        Raises
        ------
        ValueError
            If a module with the same name is already registered, or if the
            requested time-bin slot is occupied.
        """
        if module.name in self._modules:
            raise ValueError(
                f"A module named '{module.name}' is already registered. "
                "Module names must be unique."
            )
        self._register.allocate(time_bin_index, module.name)
        module._assign_time_bin(time_bin_index)
        self._modules[module.name] = module

    def registered_modules(self) -> list[QuantumHardwareModule]:
        """Return all registered hardware modules in time-bin order."""
        return sorted(
            self._modules.values(),
            key=lambda m: m.connected_time_bin or -1,
        )

    # ------------------------------------------------------------------
    # MZI mesh configuration (placeholder)
    # ------------------------------------------------------------------

    def set_mzi(self, mzi_index: int, theta: float, phi: float) -> None:
        """
        Configure one MZI in the mesh.

        Parameters
        ----------
        mzi_index:
            Which MZI to configure (0-indexed; acts between bins i and i+1).
        theta:
            New beam-splitting angle in radians.
        phi:
            New differential phase in radians.

        Raises
        ------
        IndexError
            If mzi_index is out of range.
        """
        if mzi_index < 0 or mzi_index >= len(self._mzi_mesh):
            raise IndexError(
                f"mzi_index {mzi_index} out of range [0, {len(self._mzi_mesh) - 1}]"
            )
        self._mzi_mesh[mzi_index] = MZI(theta=theta, phi=phi)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summary(self) -> str:
        """
        Return a human-readable conceptual summary of the interconnect state.

        This is intended for logging, debugging, and educational demos.
        """
        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("  Green Machine Interconnect — Status Summary")
        lines.append("=" * 60)
        lines.append(f"  Time-bin slots     : {self.n_time_bins}")
        lines.append(f"  MZI elements       : {len(self._mzi_mesh)}")
        lines.append(f"  Registered modules : {len(self._modules)}")
        lines.append("")

        if self._modules:
            lines.append("  Connected hardware modules:")
            for mod in self.registered_modules():
                tb = mod.connected_time_bin
                lines.append(
                    f"    [bin {tb:02d}]  {mod.name:<20s}  ({mod.module_type.value})"
                )
        else:
            lines.append("  No modules registered yet.")

        lines.append("")
        free = len(self._register.free_bins())
        lines.append(f"  Free time-bin slots: {free}")
        lines.append("")
        lines.append("  Protocol support (placeholder):")
        lines.append("    [✓] Boosted Bell-state measurement")
        lines.append("    [✓] Entanglement routing (conceptual)")
        lines.append("    [ ] Entanglement fusion (future work)")
        lines.append("")
        lines.append("  Distributed logical qubit:")
        if len(self._modules) >= 2:
            names = [m.name for m in self.registered_modules()]
            lines.append(
                f"    Logical qubit information can be distributed across:"
            )
            for n in names:
                lines.append(f"      - {n}")
            lines.append(
                "    Permutation-invariant encoding means partial module"
            )
            lines.append(
                "    failure does not destroy the logical qubit. (placeholder)"
            )
        else:
            lines.append("    Need >= 2 modules for distributed encoding.")
        lines.append("=" * 60)
        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"GreenMachineInterconnect("
            f"n_time_bins={self.n_time_bins}, "
            f"modules={list(self._modules.keys())})"
        )
