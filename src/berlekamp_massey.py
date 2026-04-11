def berlekamp_massey(sequence: list[int]) -> tuple[int, list[int]]:
    """Returns (linear_complexity, connection_polynomial)."""
    n = len(sequence)
    s = sequence[:]

    C = [1]
    B = [1]
    L = 0
    m = 1

    for i in range(n):
        d = s[i]
        for j in range(1, L + 1):
            if j < len(C):
                d ^= C[j] & s[i - j]
        d &= 1

        if d == 0:
            m += 1
        elif 2 * L <= i:
            T = C[:]
            padding = [0] * m
            shifted_B = padding + B
            while len(C) < len(shifted_B):
                C.append(0)
            for j in range(len(shifted_B)):
                C[j] ^= shifted_B[j]
            L = i + 1 - L
            B = T
            m = 1
        else:
            padding = [0] * m
            shifted_B = padding + B
            while len(C) < len(shifted_B):
                C.append(0)
            for j in range(len(shifted_B)):
                C[j] ^= shifted_B[j]
            m += 1

    return L, C


def linear_complexity(sequence: list[int]) -> int:
    """Returns the linear complexity (LFSR length) of the sequence."""
    lc, _ = berlekamp_massey(sequence)
    return lc


def lc_profile(sequence: list[int]) -> list[int]:
    """LC at each prefix length."""
    profile = []
    for i in range(1, len(sequence) + 1):
        profile.append(linear_complexity(sequence[:i]))
    return profile


if __name__ == "__main__":
    from lfsr import LFSR

    lfsr = LFSR(taps=[5, 2], initial_state=[1, 0, 1, 1, 0])
    seq = lfsr.generate(20)
    print(f"Sequence (20 bits): {seq}")

    lc, poly = berlekamp_massey(seq)
    print(f"Linear complexity: {lc} (true degree: {lfsr.degree})")
    print(f"Recovered poly: {poly}")

    lc_short, _ = berlekamp_massey(seq[:10])
    print(f"Complexity from first 10 bits: {lc_short}")
