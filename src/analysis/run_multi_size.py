"""
Multi-size experiment.

Generates sequences of varying length for the five generators and prints
linear complexity plus three NIST p-values (Monobit, Runs, Spectral).
Uses the same LFSR configurations as run_experiments so the output
matches the table documented in the thesis.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.lfsr import LFSR
from src.berlekamp_massey import linear_complexity
from src.generators.shrinking import shrinking_generator
from src.generators.self_shrinking import self_shrinking_generator
from src.generators.geffe import geffe_generator
from src.generators.alternating_step import alternating_step_generator

from src.tests_nist.monobit import monobit_test
from src.tests_nist.runs import runs_test
from src.tests_nist.spectral import spectral_test


SIZES = [1000, 5000, 10000, 50000]
LC_WINDOW = 5000


def _lfsr_a(): return LFSR(taps=[19,5,2,1], initial_state=[1,1,1,0,1,0,0,1,0,1,1,1,0,0,1,1,0,1,1])
def _lfsr_b(): return LFSR(taps=[17,3], initial_state=[1,0,1,1,0,1,0,1,1,0,1,1,0,1,0,1,1])
def _lfsr_c(): return LFSR(taps=[15,1], initial_state=[1,0,1,1,0,1,0,1,1,0,1,1,0,1,1])


def generate_all(n: int) -> dict[str, list[int]]:
    seqs = {}
    seqs["LFSR"]  = _lfsr_a().generate(n)
    seqs["Geffe"]      = geffe_generator(_lfsr_a(), _lfsr_b(), _lfsr_c(), n)
    seqs["Shrinking"]  = shrinking_generator(_lfsr_a(), _lfsr_b(), n)
    seqs["Self-Shrk"]  = self_shrinking_generator(_lfsr_a(), n)
    seqs["ASG"]        = alternating_step_generator(_lfsr_a(), _lfsr_b(), _lfsr_c(), n)
    return seqs


def measure(seq: list[int]) -> tuple[int, float, float, float]:
    lc = linear_complexity(seq[:LC_WINDOW])
    p_mono, _ = monobit_test(seq)
    p_runs, _ = runs_test(seq)
    p_spec, _ = spectral_test(seq)
    return lc, p_mono, p_runs, p_spec


def main():
    header = f"{'n':>7} {'gen':<12} {'LC':>6}  {'monobit':>7}  {'runs':>7}  {'espectral':>9}"
    print(header)
    print("-" * len(header))

    for n in SIZES:
        sequences = generate_all(n)
        for name, seq in sequences.items():
            lc, p_mono, p_runs, p_spec = measure(seq)
            print(f"{n:>7} {name:<12} {lc:>6}  {p_mono:>7.4f}  {p_runs:>7.4f}  {p_spec:>9.4f}")
        print()


if __name__ == "__main__":
    main()
