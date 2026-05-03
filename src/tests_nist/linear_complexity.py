"""
NIST SP 800-22 — Linear Complexity test.
Computes LC per block with Berlekamp-Massey and checks
that the values match what a random sequence would give.
"""

import math
from scipy.special import gammaincc
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.berlekamp_massey import berlekamp_massey


def linear_complexity_test(
    sequence: list[int], block_size: int = 500
) -> tuple[float, bool]:
    """Returns (p_value, passed). block_size between 500-5000, need >= 200 blocks."""
    M = block_size
    n = len(sequence)
    num_blocks = n // M

    if num_blocks < 200:
        raise ValueError(
            f"need at least {200 * M} bits for this test "
            f"(got {n})"
        )

    mu = (
        M / 2
        + (9 + (-1) ** (M + 1)) / 36
        - (M / 3 + 2 / 9) / (2 ** M)
    )

    counts = [0] * 7

    for i in range(num_blocks):
        block = sequence[i * M : (i + 1) * M]
        lc, _ = berlekamp_massey(block)

        t = (-1) ** M * (lc - mu) + 2 / 9

        if t <= -2.5:
            counts[0] += 1
        elif t <= -1.5:
            counts[1] += 1
        elif t <= -0.5:
            counts[2] += 1
        elif t <= 0.5:
            counts[3] += 1
        elif t <= 1.5:
            counts[4] += 1
        elif t <= 2.5:
            counts[5] += 1
        else:
            counts[6] += 1

    pi = [0.010417, 0.03125, 0.125, 0.5, 0.25, 0.0625, 0.020833]

    chi_sq = sum(
        (counts[i] - num_blocks * pi[i]) ** 2 / (num_blocks * pi[i])
        for i in range(7)
    )

    p_value = float(gammaincc(3, chi_sq / 2))
    return p_value, p_value >= 0.01
