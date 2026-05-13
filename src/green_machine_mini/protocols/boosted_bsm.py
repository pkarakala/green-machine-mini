"""
Boosted Bell-State Measurement (BSM) protocol.

A Bell-state measurement projects two qubits onto one of the four maximally entangled
Bell states:

    |Φ+⟩ = (|00⟩ + |11⟩) / √2
    |Φ-⟩ = (|00⟩ - |11⟩) / √2
    |Ψ+⟩ = (|01⟩ + |10⟩) / √2
    |Ψ-⟩ = (|01⟩ - |10⟩) / √2

With *linear optics only*, a BSM on two photons can succeed with at most 50%
probability. This is a fundamental theorem of linear optics (Calsamiglia & Lütkenhaus,
2001). The remaining 50% of attempts yield an ambiguous outcome that is discarded.

The **boosted** BSM in the Green Machine uses 2 dual-rail photonic qubits plus
4 ancillary single-photon modes. These ancilla modes interfere with the signal photons
before detection, allowing more Bell states to be distinguished. The ideal success
probability for this specific configuration is 75%.

This module is a *placeholder skeleton*. The success probabilities returned here are
idealized values from the paper; the actual computation of detection signatures
(scattering matrix and click-pattern decoding) is deferred to future work.

Physical accuracy note
----------------------
- The 50% linear-optics limit is physically accurate (theorem).
- The 75% boosted BSM success probability (4 ancilla modes) is the paper result.
- This code returns these as fixed placeholder values; no detection signatures
  are computed yet.

References
----------
- Ewert & van Loock, PRL 113, 140403 (2014) — near-deterministic BSM with ancilla photons
- Grice, PRA 84, 042331 (2011) — arbitrary BSM success probability with linear optics
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BellState(str, Enum):
    """The four two-qubit Bell states."""

    PHI_PLUS = "Φ+"
    PHI_MINUS = "Φ-"
    PSI_PLUS = "Ψ+"
    PSI_MINUS = "Ψ-"
    AMBIGUOUS = "ambiguous"  # Outcome that cannot be distinguished (discarded)


@dataclass
class BSMOutcome:
    """
    Result of one boosted Bell-state measurement attempt.

    Parameters
    ----------
    identified_state:
        Which Bell state was identified, or AMBIGUOUS if the attempt failed.
    success:
        True if the Bell state was unambiguously identified.
    n_ancilla_modes:
        How many ancillary single-photon modes were used in this attempt.
    success_probability:
        Ideal success probability for this configuration (placeholder value).
    """

    identified_state: BellState
    success: bool
    n_ancilla_modes: int
    success_probability: float

    def __repr__(self) -> str:
        return (
            f"BSMOutcome(state={self.identified_state.value}, "
            f"success={self.success}, "
            f"p_success={self.success_probability:.2%}, "
            f"n_ancilla_modes={self.n_ancilla_modes})"
        )


class BoostedBSM:
    """
    Placeholder implementation of the boosted Bell-state measurement protocol.

    The Green Machine boosted BSM uses 2 dual-rail photonic qubits plus ancillary
    single-photon modes stored in the time-bin delay loop. These ancilla modes
    interfere with the signal photons before detection, allowing more Bell states
    to be distinguished.

    Parameters
    ----------
    n_ancilla_modes:
        Number of ancillary single-photon modes.
        - 0 ancilla modes → standard linear-optics BSM, ideal p_success = 0.50
        - 4 ancilla modes → Green Machine boosted BSM, ideal p_success = 0.75
    """

    # Paper-accurate ideal success probabilities.
    # Real values require computing detection signatures (scattering matrix +
    # click-pattern decoding), which is not yet implemented.
    _IDEAL_SUCCESS_TABLE: dict[int, float] = {
        0: 0.50,  # standard linear-optics BSM — no ancilla (theorem limit)
        4: 0.75,  # Green Machine boosted BSM — 2 dual-rail qubits + 4 ancilla modes
    }

    def __init__(self, n_ancilla_modes: int = 4) -> None:
        if n_ancilla_modes < 0:
            raise ValueError("n_ancilla_modes must be >= 0")
        self.n_ancilla_modes = n_ancilla_modes

    @property
    def success_probability(self) -> float:
        """
        Ideal success probability for the configured number of ancilla modes.

        Values for n_ancilla_modes=0 and n_ancilla_modes=4 are paper-accurate.
        All other values use the rough placeholder formula p = 1 − (1/2)^(n/4 + 1)
        and are not physically validated.
        """
        return self._IDEAL_SUCCESS_TABLE.get(
            self.n_ancilla_modes,
            1.0 - 0.5 ** (self.n_ancilla_modes / 4 + 1),
        )

    def attempt_measurement(
        self,
        module_a_name: str,
        module_b_name: str,
    ) -> BSMOutcome:
        """
        Placeholder: attempt a boosted BSM between two registered modules.

        In a real implementation this would:
        1. Pull one photon from module_a and one from module_b into the MZI mesh.
        2. Mix them with ancilla photons from the delay loop.
        3. Record the detector click pattern.
        4. Look up the click pattern in a decoding table to identify the Bell state.

        Here we return a fixed placeholder outcome to confirm the interface works.

        Parameters
        ----------
        module_a_name:
            Name of the first hardware module.
        module_b_name:
            Name of the second hardware module.

        Returns
        -------
        BSMOutcome
            Placeholder outcome indicating the protocol ran successfully.
        """
        return BSMOutcome(
            identified_state=BellState.PHI_PLUS,
            success=True,
            n_ancilla_modes=self.n_ancilla_modes,
            success_probability=self.success_probability,
        )

    def __repr__(self) -> str:
        return (
            f"BoostedBSM("
            f"n_ancilla_modes={self.n_ancilla_modes}, "
            f"p_success={self.success_probability:.2%})"
        )
