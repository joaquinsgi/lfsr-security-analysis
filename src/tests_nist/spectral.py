"""
NIST SP 800-22 — Spectral (DFT) test.
Applies DFT and checks for dominant frequencies that
would indicate hidden periodicities.
"""

import math
import numpy as np


def spectral_test(sequence: list[int]) -> tuple[float, bool]:
    """Returns (p_value, passed)."""
    n = len(sequence)
    if n < 1000:
        raise ValueError("sequence too short, need at least 1000 bits")

    x = np.array([1 if b == 1 else -1 for b in sequence], dtype=float)

    X = np.fft.fft(x)
    magnitudes = np.abs(X[: n // 2])

    threshold = math.sqrt(math.log(1 / 0.05) * n)

    N_0 = 0.95 * n / 2
    N_1 = np.sum(magnitudes < threshold)

    d = (N_1 - N_0) / math.sqrt(n * 0.95 * 0.05 / 4)
    p_value = math.erfc(abs(d) / math.sqrt(2))

    return p_value, p_value >= 0.01
