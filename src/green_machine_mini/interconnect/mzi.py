"""
Mach-Zehnder Interferometer (MZI) — the fundamental building block of the Green Machine.

An MZI is a 2x2 linear optical element. It takes two input modes and produces two
output modes by splitting light on a beam splitter, applying a phase shift to one arm,
and recombining on a second beam splitter.

By chaining many MZIs in a mesh, you can realize an arbitrary NxN unitary
transformation on N optical modes. This is the core idea behind photonic mesh networks
like the Green Machine.

Physical accuracy note
----------------------
The unitary matrix returned by MZI.matrix() is physically grounded:
- theta controls how much the light is split (theta=pi/4 → 50/50 split)
- phi is a differential phase between the two arms

What is simplified here:
- We ignore loss, fabrication imperfections, and bandwidth effects.
- We treat the MZI as perfectly unitary (lossless).
- We use a single-frequency (monochromatic) approximation.
"""

from __future__ import annotations

import numpy as np


class MZI:
    """
    A single Mach-Zehnder Interferometer acting on two optical modes.

    The MZI implements the 2x2 unitary:

        U(theta, phi) = [ exp(i*phi)*cos(theta)  -sin(theta) ]
                        [ exp(i*phi)*sin(theta)   cos(theta) ]

    where:
    - theta in [0, pi/2] controls the power-splitting ratio
      (theta = pi/4 gives a 50/50 beam splitter)
    - phi in [0, 2*pi) is the differential arm phase

    Parameters
    ----------
    theta:
        Beam-splitting angle in radians.
    phi:
        Differential phase shift in radians.
    """

    def __init__(self, theta: float = np.pi / 4, phi: float = 0.0) -> None:
        self.theta = theta
        self.phi = phi

    def matrix(self) -> np.ndarray:
        """
        Return the 2x2 complex unitary matrix of this MZI.

        Returns
        -------
        np.ndarray
            Shape (2, 2), dtype complex128.
        """
        c = np.cos(self.theta)
        s = np.sin(self.theta)
        phase = np.exp(1j * self.phi)
        return np.array(
            [[phase * c, -s],
             [phase * s,  c]],
            dtype=complex,
        )

    def is_unitary(self, tol: float = 1e-10) -> bool:
        """
        Check that U @ U†  == I within numerical tolerance.

        Parameters
        ----------
        tol:
            Absolute tolerance for the Frobenius norm of (U @ U† - I).
        """
        u = self.matrix()
        residual = np.linalg.norm(u @ u.conj().T - np.eye(2))
        return bool(residual < tol)

    def __repr__(self) -> str:
        return f"MZI(theta={self.theta:.4f} rad, phi={self.phi:.4f} rad)"
