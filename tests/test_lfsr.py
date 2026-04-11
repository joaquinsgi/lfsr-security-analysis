"""
Tests for the LFSR class.
"""
import pytest
import sys
import os
from src.lfsr import LFSR

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_period_degree_5():
    lfsr = LFSR(taps=[5, 2], initial_state=[1, 0, 1, 1, 0])
    assert len(lfsr.full_cycle()) == 31


def test_period_degree_7():
    lfsr = LFSR(taps=[7, 6], initial_state=[1, 0, 1, 1, 0, 1, 0])
    assert len(lfsr.full_cycle()) == 127


def test_output_is_binary():
    lfsr = LFSR(taps=[5, 2], initial_state=[1, 0, 1, 1, 0])
    seq = lfsr.generate(100)
    assert all(b in (0, 1) for b in seq)


def test_reset_restores_state():
    lfsr = LFSR(taps=[5, 2], initial_state=[1, 0, 1, 1, 0])
    seq1 = lfsr.generate(20)
    lfsr.reset()
    seq2 = lfsr.generate(20)
    assert seq1 == seq2


def test_all_zero_state_raises():
    with pytest.raises(ValueError):
        LFSR(taps=[5, 2], initial_state=[0, 0, 0, 0, 0])


def test_wrong_state_length_raises():
    with pytest.raises(ValueError):
        LFSR(taps=[5, 2], initial_state=[1, 0, 1])


def test_invalid_bit_in_state_raises():
    with pytest.raises(ValueError):
        LFSR(taps=[5, 2], initial_state=[1, 0, 2, 1, 0])
