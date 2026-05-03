"""
Self-shrinking generator.

Like the shrinking generator but with a single LFSR. Takes bits
in pairs and the first bit decides if the second is output.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.lfsr import LFSR


def self_shrinking_generator(r: LFSR, n: int) -> list[int]:
    """Generates n bits from a single LFSR using self-shrinking."""
    output = []
    max_clocks = n * 10
    clocked = 0

    while len(output) < n and clocked < max_clocks:
        a = r.next_bit()
        b = r.next_bit()
        clocked += 2
        if a == 1:
            output.append(b)

    if len(output) < n:
        raise RuntimeError(
            f"could not generate {n} bits after {max_clocks} clocks"
        )

    return output


if __name__ == "__main__":
    from src.berlekamp_massey import linear_complexity

    r = LFSR(taps=[11, 2], initial_state=[1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1])

    seq_raw = r.generate(1000)
    r.reset()
    seq_ss = self_shrinking_generator(r, 1000)

    lc_raw = linear_complexity(seq_raw)
    lc_ss  = linear_complexity(seq_ss)

    print(f"Raw LFSR      → linear complexity: {lc_raw}  (degree: {r.degree})")
    print(f"Self-shrinking → linear complexity: {lc_ss}")
    print(f"Improvement factor: x{lc_ss // lc_raw}")
