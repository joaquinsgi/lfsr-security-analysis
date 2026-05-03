"""
Geffe generator.

Combines three LFSRs with a nonlinear function where R1 acts
as a selector between R2 and R3.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.lfsr import LFSR


def geffe_generator(r1: LFSR, r2: LFSR, r3: LFSR, n: int) -> list[int]:
    """Generates n bits using the Geffe generator."""
    output = []
    for _ in range(n):
        a = r1.next_bit()
        b = r2.next_bit()
        c = r3.next_bit()
        output.append((a & b) ^ ((1 ^ a) & c))
    return output


if __name__ == "__main__":
    from src.berlekamp_massey import linear_complexity

    r1 = LFSR(taps=[7, 6],    initial_state=[1, 0, 1, 1, 0, 1, 0])
    r2 = LFSR(taps=[5, 2],    initial_state=[1, 0, 1, 1, 0])
    r3 = LFSR(taps=[9, 4],    initial_state=[1, 0, 1, 1, 0, 1, 0, 1, 1])

    seqs = [r.generate(1000) for r in [r1, r2, r3]]
    for r in [r1, r2, r3]:
        r.reset()

    seq_geffe = geffe_generator(r1, r2, r3, 1000)

    for i, (r, s) in enumerate(zip([r1, r2, r3], seqs), 1):
        print(f"R{i} alone → linear complexity: {linear_complexity(s)}  (degree: {r.degree})")

    print(f"Geffe     → linear complexity: {linear_complexity(seq_geffe)}")
    print()
    print("NOTE: despite the high LC, Geffe is vulnerable to correlation attacks.")
    print("Each LFSR can be recovered independently — see security analysis.")
