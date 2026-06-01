from __future__ import annotations


class Counter:
    # Class invariant: value never decreases between two observations from
    # the same instance. The base enforces it by rejecting negative steps.
    def __init__(self, start: int = 0) -> None:
        self._value = start

    @property
    def value(self) -> int:
        return self._value

    def increment(self, by: int = 1) -> None:
        if by < 0:
            raise ValueError(f"Counter.increment requires by >= 0, got {by}")
        self._value += by


class FlexibleCounter(Counter):
    # Invariant weakening: the parent guarantees the stored value never
    # decreases. This override accepts negative steps, so callers written
    # against Counter see the value travel backwards mid-sequence.
    def increment(self, by: int = 1) -> None:
        self._value += by
