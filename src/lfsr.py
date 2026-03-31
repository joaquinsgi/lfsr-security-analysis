"""
LFSR - Linear Feedback Shift Register

A shift register where the input bit is computed as a XOR of some
positions of the register (defined by the feedback polynomial).
The sequence it generates depends entirely on the polynomial and
the initial state (seed).
"""


class LFSR:
    """
    Represents a single LFSR of degree n.

    The feedback polynomial is given as a list of tap positions
    (the degrees that participate in the XOR). For example, for
    x^5 + x^2 + 1 the taps are [5, 2].

    The initial state must have exactly n bits (no all-zeros state,
    that would make the register loop on zeros forever).
    """

    def __init__(self, taps: list[int], initial_state: list[int]):
        if not taps:
            raise ValueError("tap list cannot be empty")

        self.degree = max(taps)
        self.taps = taps

        if len(initial_state) != self.degree:
            raise ValueError(
                f"initial state must have {self.degree} bits, "
                f"got {len(initial_state)}"
            )
        if all(b == 0 for b in initial_state):
            raise ValueError("all-zero initial state is not allowed")
        if any(b not in (0, 1) for b in initial_state):
            raise ValueError("initial state must contain only 0s and 1s")

        self.state = list(initial_state)
        self._initial_state = list(initial_state)

    def _feedback_bit(self) -> int:
        """XOR of all tap positions."""
        result = 0
        for t in self.taps:
            # taps are 1-indexed from the left (position 1 = state[0])
            result ^= self.state[t - 1]
        return result

    def next_bit(self) -> int:
        """
        Advances the register by one step and returns the output bit
        (the bit that falls off the right end of the register).
        """
        output = self.state[-1]
        new_bit = self._feedback_bit()
        self.state = [new_bit] + self.state[:-1]
        return output

    def generate(self, n: int) -> list[int]:
        """Returns a sequence of n bits."""
        return [self.next_bit() for _ in range(n)]

    def full_cycle(self) -> list[int]:
        """
        Generates bits until the register returns to its initial state.
        With a primitive polynomial this gives 2^n - 1 bits.
        """
        sequence = []
        while True:
            sequence.append(self.next_bit())
            if self.state == self._initial_state:
                break
        return sequence

    def reset(self):
        """Restores the register to its initial state."""
        self.state = list(self._initial_state)

    def __repr__(self):
        return (
            f"LFSR(degree={self.degree}, taps={self.taps}, "
            f"state={self.state})"
        )


if __name__ == "__main__":
    # quick sanity check:
    # x^5 + x^2 + 1, primitive polynomial over F2
    # expected period: 2^5 - 1 = 31 bits
    lfsr = LFSR(taps=[5, 2], initial_state=[1, 0, 1, 1, 0])

    seq = lfsr.full_cycle()
    print(f"degree  : {lfsr.degree}")
    print(f"period  : {len(seq)}  (expected {2**lfsr.degree - 1})")
    print(f"sequence: {seq}")

    lfsr.reset()
    print(f"first 10 bits: {lfsr.generate(10)}")
