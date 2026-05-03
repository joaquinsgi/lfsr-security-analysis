"""
NIST SP 800-22 — Runs test.
Checks that the number of runs (consecutive equal bits)
is what you would expect from a random sequence.
"""

import math


def runs_test(sequence: list[int]) -> tuple[float, bool]:
    """Returns (p_value, passed)."""
    n = len(sequence)
    if n < 100:
        raise ValueError("sequence too short, need at least 100 bits")

    pi = sum(sequence) / n

    tau = 2 / math.sqrt(n)
    if abs(pi - 0.5) >= tau:
        return 0.0, False

    V_n = 1 + sum(
        1 for k in range(n - 1) if sequence[k] != sequence[k + 1]
    )

    numerator = abs(V_n - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    p_value = math.erfc(numerator / denominator)

    return p_value, p_value >= 0.01
