class LFSR:
    """
    Linear Feedback Shift Register (LFSR) implementation.
    """

    def __init__(self, taps: list[int], initial_state: list[int]):
        if not taps:
            raise ValueError("Tap list cannot be empty")

        self.degree = max(taps)
        self.taps = taps

        if len(initial_state) != self.degree:
            raise ValueError(
                f"Initial state must have {self.degree} bits, "
                f"Actual state: {len(initial_state)}"
            )
        if all(b == 0 for b in initial_state):
            raise ValueError("Zero initial state is not allowed")
        if any(b not in (0, 1) for b in initial_state):
            raise ValueError("Initial state must contain only 0 and 1")

        self.state = list(initial_state)
        self._initial_state = list(initial_state)

    def _feedback_bit(self) -> int:
        """XOR of all tap positions."""
        result = 0
        for t in self.taps:
            result ^= self.state[t - 1]
        return result

    def next_bit(self) -> int:
        """Clocks the register once and returns the output bit."""
        output = self.state[-1]
        new_bit = self._feedback_bit()
        self.state = [new_bit] + self.state[:-1]
        return output

    def generate(self, n: int) -> list[int]:
        """Returns a sequence of n bits."""
        return [self.next_bit() for _ in range(n)]

    def full_cycle(self) -> list[int]:
        """Generates bits until the register returns to its initial state."""
        sequence = []
        while True:
            sequence.append(self.next_bit())
            if self.state == self._initial_state:
                break
        return sequence

    def reset(self):
        self.state = list(self._initial_state)

    def __repr__(self):
        return (
            f"LFSR(degree={self.degree}, taps={self.taps}, "
            f"state={self.state})"
        )


if __name__ == "__main__":

    lfsr = LFSR(taps=[5, 2], initial_state=[1, 0, 1, 1, 0])

    seq = lfsr.full_cycle()
    print(f"Degree: {lfsr.degree}")
    print(f"Period: {len(seq)} (expected {2**lfsr.degree - 1})")
    print(f"Sequence: {seq}")

    lfsr.reset()
    print(f"First 10 bits: {lfsr.generate(10)}")
