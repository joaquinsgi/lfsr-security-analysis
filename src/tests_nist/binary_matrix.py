"""
NIST SP 800-22 — Binary Matrix Rank test.
Puts chunks of the sequence into matrices and checks
rank over GF(2). Linear structure lowers the rank.
"""

import math


_P_FULL = 0.2888
_P_FULL_1 = 0.5776
_P_REST = 0.1336


def binary_matrix_rank_test(
    sequence: list[int], rows: int = 32, cols: int = 32
) -> tuple[float, bool]:
    """Returns (p_value, passed). Needs at least 38 matrices (38*32*32 bits)."""
    n = len(sequence)
    block_size = rows * cols
    num_matrices = n // block_size

    if num_matrices < 38:
        raise ValueError(
            f"need at least {38 * block_size} bits for this test "
            f"(got {n})"
        )

    F_M = 0
    F_M1 = 0
    F_rem = 0

    for i in range(num_matrices):
        block = sequence[i * block_size : (i + 1) * block_size]
        matrix = [block[r * cols : (r + 1) * cols] for r in range(rows)]
        rank = _gf2_rank(matrix)

        if rank == rows:
            F_M += 1
        elif rank == rows - 1:
            F_M1 += 1
        else:
            F_rem += 1

    chi_sq = (
        (F_M - num_matrices * _P_FULL) ** 2 / (num_matrices * _P_FULL) +
        (F_M1 - num_matrices * _P_FULL_1) ** 2 / (num_matrices * _P_FULL_1) +
        (F_rem - num_matrices * _P_REST) ** 2 / (num_matrices * _P_REST)
    )

    p_value = math.exp(-chi_sq / 2)
    return p_value, p_value >= 0.01


def _gf2_rank(matrix: list[list[int]]) -> int:
    """Gaussian elimination over GF(2) to compute the matrix rank."""
    m = [row[:] for row in matrix]
    rows, cols = len(m), len(m[0])
    rank = 0

    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if m[row][col] == 1:
                pivot = row
                break
        if pivot is None:
            continue

        m[rank], m[pivot] = m[pivot], m[rank]

        for row in range(rows):
            if row != rank and m[row][col] == 1:
                m[row] = [m[row][k] ^ m[rank][k] for k in range(cols)]

        rank += 1

    return rank
