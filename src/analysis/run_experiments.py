"""
Runs all generators, measures LC and NIST tests,
and saves results + plots to results/.
"""

import sys
import os
import json
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.lfsr import LFSR
from src.berlekamp_massey import linear_complexity, lc_profile
from src.generators.shrinking import shrinking_generator
from src.generators.self_shrinking import self_shrinking_generator
from src.generators.geffe import geffe_generator
from src.generators.alternating_step import alternating_step_generator

from src.tests_nist.monobit import monobit_test
from src.tests_nist.block_frequency import block_frequency_test
from src.tests_nist.runs import runs_test
from src.tests_nist.binary_matrix import binary_matrix_rank_test
from src.tests_nist.maurer import maurer_test
from src.tests_nist.serial import serial_test
from src.tests_nist.spectral import spectral_test
from src.tests_nist.linear_complexity import linear_complexity_test

from src.analysis.plots import plot_lc_profile, plot_nist_comparison, plot_lc_bar

SEQ_LEN = 500_000


def _lfsr_a(): return LFSR(taps=[19,5,2,1], initial_state=[1,1,1,0,1,0,0,1,0,1,1,1,0,0,1,1,0,1,1])
def _lfsr_b(): return LFSR(taps=[17,3], initial_state=[1,0,1,1,0,1,0,1,1,0,1,1,0,1,0,1,1])
def _lfsr_c(): return LFSR(taps=[15,1], initial_state=[1,0,1,1,0,1,0,1,1,0,1,1,0,1,1])


def generate_sequences() -> dict[str, list[int]]:
    print("Generating sequences...")

    sequences = {}

    r = _lfsr_a()
    sequences["LFSR (pure)"] = r.generate(SEQ_LEN)

    sequences["Shrinking"] = shrinking_generator(_lfsr_a(), _lfsr_b(), SEQ_LEN)

    r = _lfsr_a()
    sequences["Self-Shrinking"] = self_shrinking_generator(r, SEQ_LEN)

    sequences["Geffe"] = geffe_generator(_lfsr_a(), _lfsr_b(), _lfsr_c(), SEQ_LEN)

    sequences["ASG"] = alternating_step_generator(_lfsr_a(), _lfsr_b(), _lfsr_c(), SEQ_LEN)

    print("  done.\n")
    return sequences


def run_nist_tests(seq: list[int]) -> dict[str, float]:
    results = {}

    p, _ = monobit_test(seq)
    results["Monobit"] = round(p, 4)

    p, _ = block_frequency_test(seq)
    results["Block Freq"] = round(p, 4)

    p, _ = runs_test(seq)
    results["Runs"] = round(p, 4)

    p, _ = binary_matrix_rank_test(seq)
    results["Binary Matrix"] = round(p, 4)

    p, _ = maurer_test(seq, block_size=6)
    results["Maurer"] = round(p, 4)

    (p1, p2), _ = serial_test(seq, block_size=3)
    results["Serial"] = round(min(p1, p2), 4)

    p, _ = spectral_test(seq)
    results["Spectral"] = round(p, 4)

    p, _ = linear_complexity_test(seq, block_size=500)
    results["LC Test"] = round(p, 4)

    return results


def main():
    sequences = generate_sequences()

    nist_results = {}
    lc_values = {}
    lc_profiles = {}

    for name, seq in sequences.items():
        print(f"[{name}]")
        t0 = time.time()

        nist = run_nist_tests(seq)
        nist_results[name] = nist

        lc = linear_complexity(seq[:5000])
        lc_values[name] = lc

        lc_profiles[name] = lc_profile(seq[:300])

        elapsed = time.time() - t0
        passed = sum(1 for v in nist.values() if v >= 0.01)
        print(f"  NIST: {passed}/8 passed  |  LC: {lc}  |  {elapsed:.1f}s")
        for test, pval in nist.items():
            status = "✓" if pval >= 0.01 else "✗"
            print(f"    {status} {test:<15} p={pval}")
        print()

    os.makedirs(os.path.join(os.path.dirname(__file__), "../../results"), exist_ok=True)
    results_path = os.path.join(
        os.path.dirname(__file__), "../../results/results.json"
    )
    with open(results_path, "w") as f:
        json.dump({"nist": nist_results, "lc": lc_values}, f, indent=2)
    print(f"Results saved to {results_path}\n")

    print("Generating plots...")
    plot_lc_profile(lc_profiles)
    plot_nist_comparison(nist_results)
    plot_lc_bar(lc_values)
    print("Done.")


if __name__ == "__main__":
    main()
