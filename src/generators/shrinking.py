"""
Shrinking generator.

Two LFSRs where R1 controls which bits of R2 make
it to the output, discarding the rest.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.lfsr import LFSR


def shrinking_generator(r1: LFSR, r2: LFSR, n: int) -> list[int]:
    """Generates n bits. r1 filters the output of r2."""
    output = []
    max_clocks = n * 10
    clocked = 0

    while len(output) < n and clocked < max_clocks:
        a = r1.next_bit()
        b = r2.next_bit()
        clocked += 1
        if a == 1:
            output.append(b)

    if len(output) < n:
        raise RuntimeError(
            f"could not generate {n} bits after {max_clocks} clocks — "
            "check that r1 is not stuck in a low-density state"
        )

    return output


if __name__ == "__main__":
    from src.berlekamp_massey import linear_complexity

    r1 = LFSR(taps=[7, 6], initial_state=[1, 0, 1, 1, 0, 1, 0])
    r2 = LFSR(taps=[5, 2], initial_state=[1, 0, 1, 1, 0])

    seq_r1 = r1.generate(1000)
    seq_r2 = r2.generate(1000)
    r1.reset()
    r2.reset()

    seq_shrinking = shrinking_generator(r1, r2, 1000)

    lc_r1 = linear_complexity(seq_r1)
    lc_r2 = linear_complexity(seq_r2)
    lc_sh = linear_complexity(seq_shrinking)

    print(f"R1 alone  → linear complexity: {lc_r1}  (degree: {r1.degree})")
    print(f"R2 alone  → linear complexity: {lc_r2}  (degree: {r2.degree})")
    print(f"Shrinking → linear complexity: {lc_sh}")
    print(f"Improvement factor: x{lc_sh // max(lc_r1, lc_r2)}")
