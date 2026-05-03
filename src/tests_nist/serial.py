"""
NIST SP 800-22 — Serial test.
Checks that all m-bit patterns appear with similar frequency.
"""

import math
from scipy.special import gammaincc


def serial_test(sequence: list[int], block_size: int = 3) -> tuple[tuple[float, float], bool]:
    """Returns ((p1, p2), passed). Both p-values must be >= 0.01."""
    n = len(sequence)
    m = block_size

    if 2 ** m >= n:
        raise ValueError("sequence too short for this block size")

    psi_sq_m = _psi_sq(sequence, n, m)
    psi_sq_m1 = _psi_sq(sequence, n, m - 1)
    psi_sq_m2 = _psi_sq(sequence, n, m - 2) if m >= 2 else 0.0

    del1 = psi_sq_m - psi_sq_m1
    del2 = psi_sq_m - 2 * psi_sq_m1 + psi_sq_m2

    p1 = float(gammaincc(2 ** (m - 2), del1 / 2))
    p2 = float(gammaincc(2 ** (m - 3), del2 / 2)) if m >= 2 else 1.0

    passed = p1 >= 0.01 and p2 >= 0.01
    return (p1, p2), passed


def _psi_sq(sequence: list[int], n: int, m: int) -> float:
    """Computes the psi-squared statistic for pattern length m."""
    if m == 0:
        return 0.0

    extended = sequence + sequence[: m - 1]

    counts = {}
    for i in range(n):
        pattern = tuple(extended[i : i + m])
        counts[pattern] = counts.get(pattern, 0) + 1

    psi_sq = (2 ** m / n) * sum(v ** 2 for v in counts.values()) - n
    return psi_sq
