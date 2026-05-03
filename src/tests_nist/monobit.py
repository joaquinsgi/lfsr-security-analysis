"""
NIST SP 800-22 — Frequency (Monobit) test.
Checks whether 1s and 0s are roughly balanced.
"""

import math


def monobit_test(sequence: list[int]) -> tuple[float, bool]:
    """Returns (p_value, passed). p_value >= 0.01 means pass."""
    n = len(sequence)
    if n < 100:
        raise ValueError("sequence too short, need at least 100 bits")

    S_n = sum(1 if b == 1 else -1 for b in sequence)

    s_obs = abs(S_n) / math.sqrt(n)

    p_value = math.erfc(s_obs / math.sqrt(2))

    return p_value, p_value >= 0.01
