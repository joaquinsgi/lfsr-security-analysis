"""
Berlekamp-Massey algorithm

Given a binary sequence, finds the shortest LFSR that can generate it.
The length of that LFSR is the linear complexity of the sequence.

This is exactly what an attacker would run after capturing 2*n bits
of a keystream — with just that, they can reconstruct the whole thing.
"""


def berlekamp_massey(sequence: list[int]) -> tuple[int, list[int]]:
    """
    Returns (linear_complexity, connection_polynomial) for the given
    binary sequence.

    The connection polynomial is returned as a list of coefficients
    [c0, c1, ..., cL] where c0 = 1 always.

    Example:
        complexity, poly = berlekamp_massey([1,0,1,1,0,1,0])
        # complexity is the minimum LFSR length needed
    """
    n = len(sequence)
    s = sequence[:]

    # current connection polynomial C and auxiliary polynomial B
    # both start as [1] (the trivial polynomial)
    C = [1]
    B = [1]

    L = 0   # current linear complexity estimate
    m = 1   # steps since last update
    b = 1   # leading coefficient of B at last update

    for i in range(n):
        # compute discrepancy: how wrong is our current C at step i
        d = s[i]
        for j in range(1, L + 1):
            if j < len(C):
                d ^= C[j] & s[i - j]
        d &= 1  # work in GF(2)

        if d == 0:
            # no discrepancy, just advance
            m += 1
        elif 2 * L <= i:
            # need to increase the length of the LFSR
            T = C[:]
            # C = C XOR (d/b) * x^m * B
            # in GF(2), d/b = 1 since d=b=1
            padding = [0] * m
            shifted_B = padding + B
            # extend C if necessary
            while len(C) < len(shifted_B):
                C.append(0)
            for j in range(len(shifted_B)):
                C[j] ^= shifted_B[j]
            L = i + 1 - L
            B = T
            b = d
            m = 1
        else:
            # same length suffices, just update C
            padding = [0] * m
            shifted_B = padding + B
            while len(C) < len(shifted_B):
                C.append(0)
            for j in range(len(shifted_B)):
                C[j] ^= shifted_B[j]
            m += 1

    return L, C


def linear_complexity(sequence: list[int]) -> int:
    """Returns just the linear complexity (LFSR length) of the sequence."""
    lc, _ = berlekamp_massey(sequence)
    return lc


def lc_profile(sequence: list[int]) -> list[int]:
    """
    Computes the linear complexity profile of a sequence.

    This is the linear complexity at each prefix length, so you can
    see how the complexity grows as more bits are revealed.
    Useful for spotting weaknesses visually.
    """
    profile = []
    for i in range(1, len(sequence) + 1):
        profile.append(linear_complexity(sequence[:i]))
    return profile


if __name__ == "__main__":
    from lfsr import LFSR

    # generate a short sequence and try to recover it
    lfsr = LFSR(taps=[5, 2], initial_state=[1, 0, 1, 1, 0])
    seq = lfsr.generate(20)
    print(f"sequence (20 bits): {seq}")

    # attacker only needs 2*L bits to break it
    lc, poly = berlekamp_massey(seq)
    print(f"linear complexity : {lc}  (true degree: {lfsr.degree})")
    print(f"recovered poly    : {poly}")
    print()

    # show that 2*L bits is enough — try with just 10 bits
    lc_short, _ = berlekamp_massey(seq[:10])
    print(f"complexity from first 10 bits: {lc_short}")
    print("(should already match the true degree of 5)")
