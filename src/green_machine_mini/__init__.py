"""
green-machine-mini

Educational toy model of the Green Machine photonic interconnect
for distributed modular quantum computing.

This package owns the interconnect layer only. Hardware-specific qubit
preparation (trapped-ion, NV-center, Rydberg) is intentionally out of scope.
"""

from green_machine_mini.interconnect.green_machine import GreenMachineInterconnect
from green_machine_mini.modules.module import ModuleType, QuantumHardwareModule
from green_machine_mini.protocols.boosted_bsm import BoostedBSM
from green_machine_mini.qec.distributed_w_code import DistributedLogicalQubit

__version__ = "0.1.0"

__all__ = [
    "GreenMachineInterconnect",
    "QuantumHardwareModule",
    "ModuleType",
    "BoostedBSM",
    "DistributedLogicalQubit",
]
