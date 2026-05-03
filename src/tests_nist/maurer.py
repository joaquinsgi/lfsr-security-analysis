"""
NIST SP 800-22 — Maurer's Universal Statistical test.
Measures compressibility by looking at distances between
repeated patterns. Random sequences are hard to compress.
"""

import math
from scipy.special import erfc as sc_erfc


_MAURER_PARAMS = {
    6:  {"expected": 5.2177052, "variance": 2.954},
    7:  {"expected": 6.1962507, "variance": 3.125},
    8:  {"expected": 7.1836656, "variance": 3.238},
    9:  {"expected": 8.1764248, "variance": 3.311},
    10: {"expected": 9.1723243, "variance": 3.356},
    11: {"expected": 10.170032, "variance": 3.384},
    12: {"expected": 11.168765, "variance": 3.401},
    13: {"expected": 12.168070, "variance": 3.410},
    14: {"expected": 13.167693, "variance": 3.416},
    15: {"expected": 14.167488, "variance": 3.419},
    16: {"expected": 15.167379, "variance": 3.421},
}


def maurer_test(sequence: list[int], block_size: int = 6) -> tuple[float, bool]:
    """Returns (p_value, passed). block_size=6 needs at least ~390k bits."""
    if block_size not in _MAURER_PARAMS:
        raise ValueError(f"block_size must be one of {list(_MAURER_PARAMS)}")

    n = len(sequence)
    L = block_size
    Q = 10 * (2 ** L)
    K = n // L - Q

    if K <= 0:
        raise ValueError(
            f"sequence too short for block_size={L} "
            f"(need at least {(Q + 1) * L} bits, got {n})"
        )

    table = {}
    for i in range(Q):
        block = tuple(sequence[i * L : (i + 1) * L])
        table[block] = i + 1

    total = 0.0
    for i in range(Q, Q + K):
        block = tuple(sequence[i * L : (i + 1) * L])
        if block in table:
            total += math.log2(i + 1 - table[block])
        table[block] = i + 1

    f_n = total / K

    params = _MAURER_PARAMS[L]
    c = 0.7 - 0.8 / L + (4 + 32 / L) * (K ** (-3 / L)) / 15
    sigma = c * math.sqrt(params["variance"] / K)

    p_value = float(sc_erfc(
        abs(f_n - params["expected"]) / (math.sqrt(2) * sigma)
    ))

    return p_value, p_value >= 0.01
