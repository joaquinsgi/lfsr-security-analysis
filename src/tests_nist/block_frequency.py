"""
NIST SP 800-22 — Block Frequency test.
Same as monobit but checks balance within each block.
"""

import math


def block_frequency_test(
    sequence: list[int], block_size: int = 128
) -> tuple[float, bool]:
    """Returns (p_value, passed)."""
    n = len(sequence)
    num_blocks = n // block_size

    if num_blocks < 1:
        raise ValueError(
            f"sequence too short for block size {block_size}"
        )

    proportions = []
    for i in range(num_blocks):
        block = sequence[i * block_size : (i + 1) * block_size]
        pi_i = sum(block) / block_size
        proportions.append(pi_i)

    chi_sq = 4 * block_size * sum((pi - 0.5) ** 2 for pi in proportions)

    p_value = _igamc(num_blocks / 2, chi_sq / 2)

    return p_value, p_value >= 0.01


def _igamc(a: float, x: float) -> float:
    from scipy.special import gammaincc
    return float(gammaincc(a, x))
