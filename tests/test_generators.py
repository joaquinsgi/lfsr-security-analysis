"""
Tests for the four LFSR-based generators.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.lfsr import LFSR
from src.berlekamp_massey import linear_complexity
from src.generators.shrinking import shrinking_generator
from src.generators.self_shrinking import self_shrinking_generator
from src.generators.geffe import geffe_generator
from src.generators.alternating_step import alternating_step_generator


def make_r1():
    return LFSR(taps=[7, 6], initial_state=[1, 0, 1, 1, 0, 1, 0])

def make_r2():
    return LFSR(taps=[5, 2], initial_state=[1, 0, 1, 1, 0])

def make_r3():
    return LFSR(taps=[9, 4], initial_state=[1, 0, 1, 1, 0, 1, 0, 1, 1])


def test_shrinking_output_length():
    seq = shrinking_generator(make_r1(), make_r2(), 500)
    assert len(seq) == 500

def test_shrinking_output_is_binary():
    seq = shrinking_generator(make_r1(), make_r2(), 200)
    assert all(b in (0, 1) for b in seq)

def test_shrinking_lc_greater_than_components():
    r1, r2 = make_r1(), make_r2()
    lc_combined = linear_complexity(shrinking_generator(r1, r2, 500))
    assert lc_combined > r1.degree
    assert lc_combined > r2.degree

def test_shrinking_deterministic():
    seq1 = shrinking_generator(make_r1(), make_r2(), 200)
    seq2 = shrinking_generator(make_r1(), make_r2(), 200)
    assert seq1 == seq2


def test_self_shrinking_output_length():
    r = LFSR(taps=[11, 2], initial_state=[1,0,1,1,0,1,0,1,1,0,1])
    seq = self_shrinking_generator(r, 300)
    assert len(seq) == 300

def test_self_shrinking_output_is_binary():
    r = LFSR(taps=[11, 2], initial_state=[1,0,1,1,0,1,0,1,1,0,1])
    seq = self_shrinking_generator(r, 200)
    assert all(b in (0, 1) for b in seq)

def test_self_shrinking_lc_greater_than_raw():
    r = LFSR(taps=[11, 2], initial_state=[1,0,1,1,0,1,0,1,1,0,1])
    lc_raw = linear_complexity(r.generate(500))
    r.reset()
    lc_ss = linear_complexity(self_shrinking_generator(r, 500))
    assert lc_ss > lc_raw


def test_geffe_output_length():
    seq = geffe_generator(make_r1(), make_r2(), make_r3(), 500)
    assert len(seq) == 500

def test_geffe_output_is_binary():
    seq = geffe_generator(make_r1(), make_r2(), make_r3(), 200)
    assert all(b in (0, 1) for b in seq)

def test_geffe_lc_greater_than_components():
    lc = linear_complexity(
        geffe_generator(make_r1(), make_r2(), make_r3(), 500)
    )
    assert lc > make_r1().degree
    assert lc > make_r2().degree
    assert lc > make_r3().degree


def test_asg_output_length():
    seq = alternating_step_generator(make_r1(), make_r2(), make_r3(), 300)
    assert len(seq) == 300

def test_asg_output_is_binary():
    seq = alternating_step_generator(make_r1(), make_r2(), make_r3(), 300)
    assert all(b in (0, 1) for b in seq)

def test_asg_lc_greater_than_components():
    lc = linear_complexity(
        alternating_step_generator(make_r1(), make_r2(), make_r3(), 500)
    )
    assert lc > make_r1().degree
    assert lc > make_r2().degree
    assert lc > make_r3().degree

def test_asg_deterministic():
    seq1 = alternating_step_generator(make_r1(), make_r2(), make_r3(), 200)
    seq2 = alternating_step_generator(make_r1(), make_r2(), make_r3(), 200)
    assert seq1 == seq2
