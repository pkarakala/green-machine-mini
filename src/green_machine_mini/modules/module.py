"""
Placeholder external quantum hardware endpoints.

This module defines the boundary between the Green Machine interconnect and the
physical quantum hardware that lives outside this repository. Each QuantumHardwareModule
represents one hardware node — a trapped-ion trap, an NV-center setup, a Rydberg array,
etc. — that has been prepared by an external team and is capable of emitting a photon
into the Green Machine optical channel.

What this module intentionally does NOT contain:
- Trapped-ion gate physics
- NV-center spin dynamics
- Rydberg atom interactions
- Any qubit-preparation logic

Those are owned by the hardware team. The interconnect receives photons; it does not
care how they were produced.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ModuleType(str, Enum):
    """Supported external hardware module types."""

    TRAPPED_ION = "trapped_ion"
    NV_CENTER = "nv_center"
    RYDBERG = "rydberg"
    GENERIC = "generic"


@dataclass
class PhotonEmission:
    """
    Represents the result of a hardware module emitting one photon into the interconnect.

    This is intentionally a placeholder. In a real system this would carry polarization,
    frequency, and temporal-mode information. For now it is a simple named token.
    """

    module_name: str
    module_type: ModuleType
    time_bin: int
    success: bool = True
    metadata: dict = field(default_factory=dict)

    def __repr__(self) -> str:
        status = "OK" if self.success else "FAILED"
        return (
            f"PhotonEmission(from={self.module_name!r}, "
            f"type={self.module_type.value}, "
            f"time_bin={self.time_bin}, "
            f"status={status})"
        )


class QuantumHardwareModule:
    """
    Placeholder endpoint representing one external quantum hardware node.

    A QuantumHardwareModule is the abstraction that the Green Machine interconnect
    uses to refer to a physically separate quantum processor. The interconnect does
    not know — and does not need to know — how the qubit was prepared inside that
    processor. It only needs to know:

    1. That the module *exists* and has a name.
    2. That the module can *emit a photon* at a requested time bin.
    3. That the module can *receive a classical signal* (e.g., BSM outcome) to apply
       a Pauli correction (feedforward) — placeholder for future work.

    Hardware-specific qubit preparation is intentionally out of scope here.

    Parameters
    ----------
    name:
        Human-readable label (e.g. "trapped_ion_A").
    module_type:
        Category of the underlying hardware platform.
    """

    def __init__(self, name: str, module_type: ModuleType = ModuleType.GENERIC) -> None:
        self.name = name
        self.module_type = module_type
        self._connected_time_bin: int | None = None

    @property
    def connected_time_bin(self) -> int | None:
        """The time-bin slot this module is registered to in the interconnect."""
        return self._connected_time_bin

    def _assign_time_bin(self, time_bin: int) -> None:
        """Called by the interconnect during module registration."""
        self._connected_time_bin = time_bin

    def emit_photon(self) -> PhotonEmission:
        """
        Placeholder: request the module to emit one photon into the interconnect.

        In a real system this would trigger hardware-specific logic (e.g., exciting
        an ion and collecting the emitted photon into a fiber). Here it returns a
        placeholder emission token.

        Returns
        -------
        PhotonEmission
            A descriptor of the emitted photon (placeholder values).

        Raises
        ------
        RuntimeError
            If the module has not been registered with an interconnect yet.
        """
        if self._connected_time_bin is None:
            raise RuntimeError(
                f"Module '{self.name}' has not been registered with an interconnect. "
                "Call GreenMachineInterconnect.register_module() first."
            )
        return PhotonEmission(
            module_name=self.name,
            module_type=self.module_type,
            time_bin=self._connected_time_bin,
        )

    def receive_classical_signal(self, signal: dict) -> None:
        """
        Placeholder: receive a classical feedforward signal from the interconnect.

        After a Bell-state measurement, the BSM outcome must be sent classically to
        the participating modules so they can apply a Pauli correction to their qubit.
        This method is the entry point for that signal on the hardware side.

        Parameters
        ----------
        signal:
            Dictionary carrying the BSM outcome (placeholder structure).
        """
        # Placeholder — hardware team implements the Pauli correction here.
        pass

    def __repr__(self) -> str:
        tb = self._connected_time_bin
        slot = f"time_bin={tb}" if tb is not None else "unregistered"
        return f"QuantumHardwareModule(name={self.name!r}, type={self.module_type.value}, {slot})"
