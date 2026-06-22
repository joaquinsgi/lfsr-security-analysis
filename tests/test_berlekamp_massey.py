"""
Tests for the Berlekamp-Massey algorithm.
"""
from src.berlekamp_massey import berlekamp_massey, linear_complexity, lc_profile
from src.lfsr import LFSR


def test_lc_matches_lfsr_degree():
    lfsr = LFSR(taps=[5, 2], initial_state=[1, 0, 1, 1, 0])
    seq = lfsr.full_cycle()
    assert linear_complexity(seq) == 5


def test_lc_recovered_from_2n_bits():
    lfsr = LFSR(taps=[7, 6], initial_state=[1, 0, 1, 1, 0, 1, 0])
    seq = lfsr.generate(14)
    assert linear_complexity(seq) == 7


def test_constant_sequence_has_lc_1():
    assert linear_complexity([1] * 20) == 1


def test_alternating_sequence():
    seq = [i % 2 for i in range(20)]
    assert linear_complexity(seq) == 2


def test_lc_profile_is_non_decreasing():
    lfsr = LFSR(taps=[5, 2], initial_state=[1, 0, 1, 1, 0])
    seq = lfsr.generate(40)
    profile = lc_profile(seq)
    for i in range(1, len(profile)):
        assert profile[i] >= profile[i - 1]


def test_poly_first_coeff_is_1():
    lfsr = LFSR(taps=[5, 2], initial_state=[1, 0, 1, 1, 0])
    seq = lfsr.generate(20)
    _, poly = berlekamp_massey(seq)
    assert poly[0] == 1
