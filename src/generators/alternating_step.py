"""
Alternating Step Generator (ASG).

Three LFSRs where R1 controls which of R2 or R3 advances
on each clock cycle. Output is the XOR of R2 and R3.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.lfsr import LFSR


def alternating_step_generator(r1: LFSR, r2: LFSR, r3: LFSR, n: int) -> list[int]:
    """Generates n bits. r1 decides which of r2/r3 advances."""
    output = []

    b2 = r2.next_bit()
    b3 = r3.next_bit()

    for _ in range(n):
        a = r1.next_bit()
        if a == 1:
            b2 = r2.next_bit()
        else:
            b3 = r3.next_bit()
        output.append(b2 ^ b3)

    return output


if __name__ == "__main__":
    from src.berlekamp_massey import linear_complexity

    r1 = LFSR(taps=[7, 6],    initial_state=[1, 0, 1, 1, 0, 1, 0])
    r2 = LFSR(taps=[5, 2],    initial_state=[1, 0, 1, 1, 0])
    r3 = LFSR(taps=[9, 4],    initial_state=[1, 0, 1, 1, 0, 1, 0, 1, 1])

    seqs = [r.generate(1000) for r in [r1, r2, r3]]
    for r in [r1, r2, r3]:
        r.reset()

    seq_asg = alternating_step_generator(r1, r2, r3, 1000)

    for i, (r, s) in enumerate(zip([r1, r2, r3], seqs), 1):
        print(f"R{i} alone → linear complexity: {linear_complexity(s)}  (degree: {r.degree})")

    print(f"ASG       → linear complexity: {linear_complexity(seq_asg)}")
