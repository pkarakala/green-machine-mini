"""
Time-bin mode management for the Green Machine interconnect.

In the Green Machine architecture, a single spatial optical mode is reused across
many time slots — called *time bins*. Each time bin carries one photon (or vacuum)
traveling through the same physical fiber or waveguide, separated in time rather than
in space.

This time-multiplexing strategy is what makes the Green Machine hardware-efficient:
instead of needing N separate fibers to connect N modules, a single delay-loop fiber
suffices, with photons entering at different times.

Physical accuracy note
----------------------
- We model time bins as discrete integer-indexed slots. Real implementations have a
  continuous time axis; we discretize for simplicity.
- We ignore photon loss in the delay loop.
- We ignore timing jitter and clock synchronization errors.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TimeBin:
    """
    One time-bin slot in the Green Machine optical channel.

    Parameters
    ----------
    index:
        Integer slot index (0-based).
    occupied:
        Whether this bin has been assigned to a hardware module.
    module_name:
        Name of the module occupying this bin, or None if empty.
    """

    index: int
    occupied: bool = False
    module_name: str | None = None

    def __repr__(self) -> str:
        if self.occupied:
            return f"TimeBin(index={self.index}, module={self.module_name!r})"
        return f"TimeBin(index={self.index}, empty)"


class TimeBinRegister:
    """
    Registry of all time-bin slots available in the Green Machine channel.

    This class tracks which bins are free, which are claimed by hardware modules,
    and provides allocation logic for the interconnect.

    Parameters
    ----------
    n_bins:
        Total number of time-bin slots in this interconnect instance.
    """

    def __init__(self, n_bins: int) -> None:
        if n_bins < 1:
            raise ValueError(f"n_bins must be >= 1, got {n_bins}")
        self.n_bins = n_bins
        self._bins: list[TimeBin] = [TimeBin(index=i) for i in range(n_bins)]

    def allocate(self, bin_index: int, module_name: str) -> TimeBin:
        """
        Assign a time-bin slot to a named hardware module.

        Parameters
        ----------
        bin_index:
            The slot index to claim.
        module_name:
            The name of the module claiming this slot.

        Returns
        -------
        TimeBin
            The updated TimeBin object.

        Raises
        ------
        IndexError
            If bin_index is out of range.
        ValueError
            If the slot is already occupied.
        """
        if bin_index < 0 or bin_index >= self.n_bins:
            raise IndexError(
                f"bin_index {bin_index} is out of range [0, {self.n_bins - 1}]"
            )
        slot = self._bins[bin_index]
        if slot.occupied:
            raise ValueError(
                f"Time bin {bin_index} is already occupied by '{slot.module_name}'. "
                "Each module needs its own time-bin slot."
            )
        slot.occupied = True
        slot.module_name = module_name
        return slot

    def free_bins(self) -> list[TimeBin]:
        """Return all unoccupied time-bin slots."""
        return [b for b in self._bins if not b.occupied]

    def occupied_bins(self) -> list[TimeBin]:
        """Return all occupied time-bin slots."""
        return [b for b in self._bins if b.occupied]

    def get_bin(self, index: int) -> TimeBin:
        """Look up a single time bin by index."""
        if index < 0 or index >= self.n_bins:
            raise IndexError(f"bin_index {index} is out of range [0, {self.n_bins - 1}]")
        return self._bins[index]

    def __repr__(self) -> str:
        used = len(self.occupied_bins())
        return f"TimeBinRegister(n_bins={self.n_bins}, occupied={used}, free={self.n_bins - used})"
